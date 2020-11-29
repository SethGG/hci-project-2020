class Config():
    SECRET_KEY = 'n983U#!*TPiu'
    SQLALCHEMY_BINDS = {
        'spellbook': 'sqlite:///spellbook.db',
        'user_data': 'sqlite:///user_data.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
