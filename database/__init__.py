from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from database.spellbook import Spell
from database.user_data import User, Character, Prepared
