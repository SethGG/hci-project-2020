from routes import routes
from flask import render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from database.spellbook import Spell


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


@routes.route('/spellbook', methods=['GET', 'POST'])
def spellbook():
    session['active page'] = '.spellbook'
    form = SpellbookForm(request.args, csrf_enabled=False)
    total_query = Spell.query
    if form.validate():
        print('yeet')
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
    print(form.errors)
    return render_template('spellbook.html', title='Spellbook', form=form, table=table)
