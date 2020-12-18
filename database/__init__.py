from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

from database.spellbook import Spell
from database.user_data import User, Character, Prepared
