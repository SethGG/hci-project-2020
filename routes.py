from database import db
from database.user_data import User
from database.spellbook import Spell
from forms import LoginForm, SpellbookForm
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_user, logout_user
from flask_bootstrap import Bootstrap

routes = Blueprint('routes', __name__)
bootstrap = Bootstrap()

#########
# Pages #
#########


@routes.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('.user', username=current_user.username))
    form = LoginForm()
    form2 = LoginForm()
    return render_template('root.html', title='Home Page', form=form, form2=form2)


@routes.route('/user/<username>')
def user(username):
    if not current_user.is_authenticated:
        return redirect(url_for('.root'))
    elif current_user.username != username:
        return redirect(url_for('.user', username=current_user.username))
    return(current_user.username)


@routes.route('/spellbook')
def spellbook():
    form = SpellbookForm(request.args, csrf_enabled=False)
    total_query = Spell.query
    if form.validate():
        for field, column in form.db_match:
            if field.data:
                build_query = Spell.query.filter(False)
                if isinstance(field.data, list):
                    for selection in field.data:
                        build_query = build_query.union(total_query.filter(column == selection))
                if isinstance(field.data, str):
                    build_query = total_query.filter(column.contains(field.data))
                total_query = build_query

    table = total_query.all()
    return render_template('spellbook.html', title='Spellbook', filterform=form, table=table,
                           current_user=current_user, loginform=LoginForm())


#############
# Login API #
#############

@routes.route('/login', methods=['POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.get(form.username.data)
            if user is None or user.password != form.password.data:
                return "Username or password is wrong", 400
            login_user(user)
            return "Succesfully logged in", 200
        return "Validation error", 400
    return "User is already logged in", 400


@routes.route('/register', methods=['POST'])
def register():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            usernames = [x[0] for x in User.query.with_entities(User.username).all()]
            if form.username.data in usernames:
                return "Username is already in use", 400
            if form.username.data not in usernames:
                user = User(username=form.username.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return "Succesfully registered and logged in", 200
        return "Validation error", 400
    return "User is already loggin in", 400


@routes.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return "Succesfully logged out", 200
    else:
        return "User not logged in", 400
