from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    username = db.Column(db.String(20), primary_key=True, index=True)
    password = db.Column(db.String(60), nullable=False)

    characters = db.relationship("Character")


class Character(db.Model):
    __tablename__ = "character"

    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(20), db.ForeignKey('user.username'))
#   avatar = image

    spell_mod = db.Column(db.Integer, default=0)
    spell_dc = db.Column(db.Integer, default=0)
    cantrip_lvl = db.Column(db.Integer, default=0)

    spell_slots_0 = db.Column(db.Integer, default=0)
    spell_slots_1 = db.Column(db.Integer, default=0)
    spell_slots_2 = db.Column(db.Integer, default=0)
    spell_slots_3 = db.Column(db.Integer, default=0)
    spell_slots_4 = db.Column(db.Integer, default=0)
    spell_slots_5 = db.Column(db.Integer, default=0)
    spell_slots_6 = db.Column(db.Integer, default=0)
    spell_slots_7 = db.Column(db.Integer, default=0)
    spell_slots_8 = db.Column(db.Integer, default=0)
    spell_slots_9 = db.Column(db.Integer, default=0)
    spell_slots_10 = db.Column(db.Integer, default=0)

    prepared_spells = db.relationship("Prepared")


class Prepared(db.Model):
    __tablename__ = "prepared"

    pid = db.Column(db.Integer, primary_key=True)
    char_name = db.Column(db.String(20), db.ForeignKey("character.name"))
    spell_name = db.Column(db.String(20))
    spell_level = db.Column(db.Integer)


spellbook_db = SQLAlchemy()


class Spell(spellbook_db.Model):
    __tablename__ = "spell"

    name = db.Column(db.String(20), primary_key=True)
    level = db.Column(db.Integer)
    actions = db.Column(db.String(20))
    save = db.Column(db.String(20))
    school = db.Column(db.String(20))
    targets = db.Column(db.String(20))
    rarity = db.Column(db.String(20))
    summary = db.Column(db.String(200))

    traditions = db.relationship("Spell_has_Tradition")


class Spell_has_Tradition(spellbook_db.Model):
    __tablename__ = "spell_has_tradition"

    spell_name = db.Column(db.String(20), db.ForeignKey('spell.name'), primary_key=True)
    tradition = db.Column(db.String(20), primary_key=True)


class Spell_has_Component(spellbook_db.Model):
    __tablename__ = "spell_has_component"

    spell_name = db.Column(db.String(20), db.ForeignKey('spell.name'), primary_key=True)
    component = db.Column(db.String(20), primary_key=True)


class Spell_has_Trait(spellbook_db.Model):
    __tablename__ = "spell_has_trait"

    spell_name = db.Column(db.String(20), db.ForeignKey('spell.name'), primary_key=True)
    trait = db.Column(db.String(20), primary_key=True)
