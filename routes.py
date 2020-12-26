from database import db
from database.user_data import User, Character, Prepared
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
    return render_template('user.html', title='User Page', user=current_user)


@routes.route('/user/<username>/<cid>', methods=['GET'])
def character(username, cid):
    if not current_user.is_authenticated:
        return redirect(url_for('.root'))
    if current_user.username != username or cid not in [str(x.cid) for x in current_user.characters]:
        return redirect(url_for('.user', username=current_user.username))
    char = Character.query.get(int(cid))
    return render_template('character.html', title='Character Page', char=char)


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
            spell = Spell.query.get(form.spell.data)
            char = Character.query.get(form.character.data)
            prepare = []
            for level, field, column in form.db_match:
                if spell.level == "cantrip" and level != "cantrip" and int(field.data) > 0:
                    return "You can only prepare cantrips in cantrip slots", 400
                if spell.level != "cantrip" and level != "cantrip" and int(spell.level) > int(level):
                    return "You cannot prepare this spell in a slot lower than lv. %s" % spell.level, 400
                if spell.level != "cantrip" and level == "cantrio" and field.data > 0:
                    return "You cannot prepare leveled spells in cantrip slots", 400

                max_slots = getattr(char, "spell_slots_%s" % level)
                taken_slots = len([x for x in char.prepared_spells if x.spell_slot_level == level])
                if taken_slots + int(field.data) > max_slots:
                    return "You do not have enough spell slots", 400

                for i in range(int(field.data)):
                    prepare.append(Prepared(cid=char.cid, sid=spell.id, spell_slot_level=level))
            for p in prepare:
                db.session.add(p)
                db.session.commit()
            return "Succesfully prepred spells", 200
        return "Validation error", 400
    else:
        return "User not logged in", 400
