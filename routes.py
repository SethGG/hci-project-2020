from database import db
from database.user_data import User, Character
from database.spellbook import Spell
from forms import LoginForm, SpellbookForm, PrepareForm
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from flask_bootstrap import Bootstrap

routes = Blueprint('routes', __name__)
bootstrap = Bootstrap()


#########
# Pages #
#########

@routes.route('/', methods=['GET'])
def root():
    if current_user.is_authenticated:
        return redirect(url_for('.user', username=current_user.username))
    return render_template('root.html', title='Home Page', loginform=LoginForm())


@routes.route('/user/<username>', methods=['GET'])
def user(username):
    if not current_user.is_authenticated:
        return redirect(url_for('.root'))
    elif current_user.username != username:
        return redirect(url_for('.user', username=current_user.username))
    return(current_user.username)


@routes.route('/spellbook', methods=['GET'])
def spellbook():
    filterform = SpellbookForm(request.args, csrf_enabled=False)
    total_query = Spell.query
    if filterform.validate():
        for field, column in filterform.db_match:
            if field.data:
                build_query = Spell.query.filter(False)
                if isinstance(field.data, list):
                    for selection in field.data:
                        build_query = build_query.union(total_query.filter(column == selection))
                if isinstance(field.data, str):
                    build_query = total_query.filter(column.contains(field.data))
                total_query = build_query

    def custom_sort(x):
        try:
            return [int(x.level) + 122] + [ord(y) for y in x.name]
        except ValueError:
            return [ord(y) for y in x.level] + [ord(y) for y in x.name]
    table = sorted(total_query.all(), key=custom_sort)

    if current_user.is_authenticated:
        return render_template('spellbook.html', title='Spellbook', filterform=filterform,
                               table=table, prepareform=PrepareForm(current_user))
    else:
        return render_template('spellbook.html', title='Spellbook', filterform=filterform,
                               table=table, loginform=LoginForm())


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
                char = Character(name="Demo Character", owner=form.username.data)
                db.session.add(char)
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


#################
# Character API #
#################

@routes.route('/prepare', methods=['POST'])
def prepare():
    if current_user.is_authenticated:
        form = PrepareForm(current_user)
        if form.validate_on_submit():
            return "Valid", 200
        return form.errors, 400
    else:
        return "User not logged in", 400