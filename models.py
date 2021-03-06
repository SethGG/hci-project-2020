from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

db = SQLAlchemy()
login = LoginManager()


@login.user_loader
def load_user(name):
    return User.query.get(name)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    username = db.Column(db.String(20), primary_key=True, index=True)
    password = db.Column(db.String(20), nullable=False)

    characters = db.relationship("Character")

    def get_id(self):
        return self.username


class Character(db.Model):
    __tablename__ = "character"

    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(20), db.ForeignKey('user.username'))
#   avatar = image

    spell_mod = db.Column(db.Integer, default=0)
    spell_dc = db.Column(db.Integer, default=0)
    cantrip_lvl = db.Column(db.Integer, default=0)

    spell_slots_cantrip = db.Column(db.Integer, default=5)
    spell_slots_1 = db.Column(db.Integer, default=2)
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
    cid = db.Column(db.Integer, db.ForeignKey("character.cid"))
    sid = db.Column(db.Integer, db.ForeignKey("spell.sid"))
    spell_slot_level = db.Column(db.String(20))
    used = db.Column(db.Boolean, default=False)

    spell = db.relationship("Spell")


class Spell(db.Model):
    __tablename__ = "spell"

    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    level = db.Column(db.String)
    traditions = db.Column(db.String)
    actions = db.Column(db.String)
    components = db.Column(db.String)
    save = db.Column(db.String)
    school = db.Column(db.String)
    targets = db.Column(db.String)
    rarity = db.Column(db.String)
    traits = db.Column(db.String)
    summary = db.Column(db.String)
    description = db.Column(db.String)
    heightened_plus1 = db.Column('heightened_+1', db.String)
    heightened_plus2 = db.Column('heightened_+2', db.String)
    heightened_plus3 = db.Column('heightened_+3', db.String)
    heightened_2nd = db.Column(db.String)
    heightened_3rd = db.Column(db.String)
    heightened_4th = db.Column(db.String)
    heightened_5th = db.Column(db.String)
    heightened_6th = db.Column(db.String)
    heightened_7th = db.Column(db.String)
    heightened_8th = db.Column(db.String)
    heightened_9th = db.Column(db.String)
    heightened_10th = db.Column(db.String)


def rebuild():
    headers = {
        'authority': 'pf2.easytool.es',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://pf2.easytool.es',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pf2.easytool.es/spellbook/',
        'accept-language': 'en-US,en;q=0.9,nl;q=0.8',
        'cookie': 'PHPSESSID=k5bds782h4d77fma3drk8f1o6r',
    }

    data = {
        'caca': '{"traditions":["1182","1184","1183","1185"],"schools":["25","56","70","84","88","114","139","179"],"actions":["Reaction","action1","action2","action3","1 minute","5 minutes","10 minutes","1 hour"],"traits":["26","28","38","39","1426","48","50","57","61","62","63","66","69","78","79","83","87","90","91","95","98","99","100","105","111","115","122","123","128","132","135","136","140","1202","147","148","149","150","151","154","160","163","165","167","169","178","185","187"],"rarity":["0","181","159"],"target":["0","1","2","3"],"level":["0","1","2","3","4","5","6","7","8","9","10"],"sources":["5","8194","9","4306","9957","12","4795","4796","4797","4798","6726","7292","7509","7511"],"text":""}',
        'H': 'false',
        'Traits': '0',
        'Checked': '[]',
        'FocusSpell': '0',
        'cantripLvl': '1'
    }

    # Request full spell list from pf2.easytools.es
    response = requests.post('https://pf2.easytool.es/spellbook/table.php',
                             headers=headers, data=data)
    response.encoding = 'utf-8'

    # Replace the missing actions icons with it's description
    fix_actions = re.compile(
        r'<i class="pf2 (?:Reaction|action\d)" data-toggle="tooltip" title="(Reaction|Single Action|Two-Action Activity|Three-Action Activity)"></i>')
    fixed_table = fix_actions.sub(r'\1', response.text)

    # Generate a list of the spell ids
    find_id = re.compile(r"<input type='hidden' class='id' value='(\d+)'>")
    ids = find_id.findall(fixed_table)

    # Generate dataframe from html table
    df = pd.read_html(fixed_table)[0].dropna(how='all', axis='columns')
    df.rename(columns={'Traditions*': 'Traditions', 'School*': 'School'}, inplace=True)
    df.insert(0, 'sid', ids)
    df.set_index('sid', inplace=True)

    # Loop over spells to get additional information
    df['description'] = ""
    for id in ids:
        headers = {
            'authority': 'pf2.easytool.es',
            'accept': 'text/html, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://pf2.easytool.es',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://pf2.easytool.es/spellbook/',
            'accept-language': 'en-US,en;q=0.9,nl;q=0.8',
        }

        data = {
            'id_feature': id,
            'CP': '0',
            'type': '1',
            'optional': 'optundefined'
        }

        response = requests.post('https://pf2.easytool.es/php/actionInfo.php',
                                 headers=headers, data=data)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        desc = soup.find('section', class_="content")
        height = soup.find('section', class_="content extra")

        if desc:
            df.at[id, 'description'] = desc.text
        if height:
            pars = height.find_all('p', class_="gris")
            for par in pars:
                find_lvl = re.compile(r'Heightened \((.+?)\)')
                match = find_lvl.match(par.strong.text)
                lvl = match.group(1)
                if 'heightened_' + lvl not in df:
                    df['heightened_' + lvl] = ""
                df.at[id, 'heightened_' + lvl] = par.text.lstrip(match.group(0))

    # Drop and recreate table
    Spell.__table__.drop(db.engine)
    Spell.__table__.create(db.engine)

    # Popupate database from dataframe
    df.to_sql('spell', con=db.get_engine(), if_exists='append')
