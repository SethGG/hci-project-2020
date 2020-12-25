from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
from database.spellbook import Spell


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')


class SpellbookForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        def custom_sort(x):
            try:
                return [int(x[0]) + 122]
            except ValueError:
                return [ord(y) for y in x[0]]

        super().__init__(*args, **kwargs)
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
