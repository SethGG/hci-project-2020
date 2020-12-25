from flask import Flask
from config import Config
from database import db, login
from routes import routes, bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login.init_app(app)
bootstrap.init_app(app)
app.register_blueprint(routes)
app.app_context().push()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
