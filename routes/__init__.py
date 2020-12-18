from flask import Blueprint
from flask_bootstrap import Bootstrap

routes = Blueprint('routes', __name__)
bootstrap = Bootstrap()

from routes.root import root, login
from routes.spellbook import spellbook
