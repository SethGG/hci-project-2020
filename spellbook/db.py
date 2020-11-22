from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///spellbook.db', echo=False)
Session = scoped_session(sessionmaker(bind=engine))
