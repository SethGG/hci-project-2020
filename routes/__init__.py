from flask import Blueprint

routes = Blueprint('routes', __name__)

from routes.root import root, login
