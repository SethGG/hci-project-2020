from routes import routes
from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
from database.spellbook import Spell
from flask_table import Table, Col


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


@routes.route('/')
def root():
    return 'Home Page'


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('routes.root'))
    return render_template('login.html', title='Sign In', form=form)


class SpellbookForm(FlaskForm):
    def __init__(self):
        def custom_sort(x):
            try:
                return [int(x[0]) + 122]
            except ValueError:
                return [ord(y) for y in x[0]]

        super().__init__()
        self.db_match = [(f[1], c[1]) for f in vars(self).items()
                         for c in vars(Spell).items() if f[0] == c[0] and '_' not in f[0]]
        for field, column in self.db_match:
            field.choices = {(x[0], x[0]) for x in Spell.query.with_entities(
                column).distinct().all()}
            field.choices = sorted(field.choices, key=custom_sort)

    level = SelectMultipleField('Level')
    traditions = SelectMultipleField('Traditions')
    actions = SelectMultipleField('Actions')
    components = SelectMultipleField('Components')
    save = SelectMultipleField('Save')
    school = SelectMultipleField('School')
    targets = SelectMultipleField('Targets')
    rarity = SelectMultipleField('Rarity')
    traits = SelectMultipleField('Traits')
    name = StringField('Name')
    submit = SubmitField('Filter')


class SpellTable(Table):
    name = Col('Name')
    level = Col('Level')
    traditions = Col('Traditions')
    actions = Col('Actions')
    components = Col('Components')
    save = Col('Save')
    school = Col('School')
    targets = Col('Targets')
    rarity = Col('Rarity')
    traits = Col('Traits')


@routes.route('/spellbook', methods=['GET', 'POST'])
def spellbook():
    form = SpellbookForm()
    total_query = Spell.query
    if form.validate_on_submit():
        for field, column in form.db_match:
            if field.data:
                build_query = Spell.query.filter(False)
                if isinstance(field.data, list):
                    for selection in field.data:
                        build_query = build_query.union(total_query.filter(column == selection))
                if isinstance(field.data, str):
                    build_query = total_query.filter(column.contains(field.data))
                total_query = build_query

    table = SpellTable(total_query.all(), border=True)
    return render_template('spellbook.html', title='Spellbook', form=form, table=table)
