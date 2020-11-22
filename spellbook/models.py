from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Spell(Base):
    __tablename__ = 'spells'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(String)
    traditions = Column(String)
    actions = Column(String)
    components = Column(String)
    save = Column(String)
    school = Column(String)
    targets = Column(String)
    rarity = Column(String)
    traits = Column(String)
    summary = Column(String)

    def __repr__(self):
        return "<Spell(%s)>" % self.Name
