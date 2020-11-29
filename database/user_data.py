from database import db


class User(db.Model):
    __bind_key__ = 'user_data'
    __tablename__ = "user"

    username = db.Column(db.String(20), primary_key=True, index=True)
    password = db.Column(db.String(20), nullable=False)

    characters = db.relationship("Character")


class Character(db.Model):
    __bind_key__ = 'user_data'
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
    __bind_key__ = 'user_data'
    __tablename__ = "prepared"

    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.String(20), db.ForeignKey("character.cid"))
    spell_name = db.Column(db.String(20))
    spell_level = db.Column(db.Integer)
