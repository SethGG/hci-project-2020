from routes import routes
from database import db
from database.user_data import User
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


@routes.route('/')
def root():
    session['active page'] = '.root'
    if current_user.is_authenticated:
        return redirect(url_for('.user', username=current_user.username))
    form = LoginForm()
    form2 = LoginForm()
    return render_template('root.html', title='Home Page', form=form, form2=form2)


@routes.route('/user/<username>')
def user(username):
    session['active page'] = '.user'
    if not current_user.is_authenticated:
        return redirect(url_for('.root'))
    elif current_user.username != username:
        return redirect(url_for('.user', username=current_user.username))
    return(current_user.username)


@routes.route('/register', methods=['POST'])
def register():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            usernames = [x[0] for x in User.query.with_entities(User.username).all()]
            if form.username.data in usernames:
                flash('Username is already in use')
                return redirect(url_for('.root'))
            if form.username.data not in usernames:
                db.session.add(User(username=form.username.data, password=form.password.data))
                db.session.commit()
                return login(form=form)


@routes.route('/login', methods=['POST'])
def login(form=None):
    if not current_user.is_authenticated:
        if not form:
            form = LoginForm()
        if form.validate_on_submit():
            user = User.query.get(form.username.data)
            if user is None or user.password != form.password.data:
                flash('Invalid username or password')
                return redirect(url_for(session['active page']))
            login_user(user)
            return redirect(url_for('.user', username=current_user.username))
    return redirect(url_for(session['active page']))


@routes.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for(session['active page']))
