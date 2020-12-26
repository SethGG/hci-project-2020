from flask import Flask
from config import Config
from database import db, login
from database.spellbook import rebuild
from routes import routes, bootstrap
import argparse

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login.init_app(app)
bootstrap.init_app(app)
app.register_blueprint(routes)
app.app_context().push()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rebuild', help='Rebuild spell database', action="store_true")
    args = parser.parse_args()
    if args.rebuild:
        rebuild()
    db.create_all(bind="user_data")
    app.run(host='0.0.0.0', debug=True)
