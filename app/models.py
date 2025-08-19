from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    hp = Column(Integer, default=100)
    atk = Column(Integer, default=10)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    gold = Column(Integer, default=0)
    weapon_level = Column(Integer, default=1)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    cost = Column(Integer)
    atk_bonus = Column(Integer, default=0)
    hp_bonus = Column(Integer, default=0)
