from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField, IntegerField
from wtforms.validators import DataRequired
from database.spellbook import Spell
from database.user_data import Character


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


class PrepareForm(FlaskForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character.choices = [(x.cid, x.name) for x in user.characters]
        self.spell.choices = [x[0] for x in Spell.query.with_entities(Spell.id)]
        self.db_match = [(f[0].lstrip("lv"), f[1], c[1]) for f in vars(self).items()
                         for c in vars(Character).items()
                         if f[0].lstrip("lv") == c[0].lstrip("spell_slots_") and '_' not in f[0]]

    character = SelectField('Character')
    spell = IntegerField('Spell ID')
    cantrip = SelectField('Cantrip', choices=list(range(5)))
    lv1 = SelectField('Lv. 1', choices=list(range(5)))
    lv2 = SelectField('Lv. 2', choices=list(range(5)))
    lv3 = SelectField('Lv. 3', choices=list(range(5)))
    lv4 = SelectField('Lv. 4', choices=list(range(5)))
    lv5 = SelectField('Lv. 5', choices=list(range(5)))
    lv6 = SelectField('Lv. 6', choices=list(range(5)))
    lv7 = SelectField('Lv. 7', choices=list(range(5)))
    lv8 = SelectField('Lv. 8', choices=list(range(5)))
    lv9 = SelectField('Lv. 9', choices=list(range(5)))
    lv10 = SelectField('Lv. 10', choices=list(range(5)))
    submit = SubmitField('Confirm')
