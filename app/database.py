import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Player, Item

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./game.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if not db.get(Player, 1):
            db.add(Player(id=1))
        if db.query(Item).count() == 0:
            db.add_all([
                Item(name="Health Potion", cost=20, hp_bonus=20),
                Item(name="Iron Sword", cost=50, atk_bonus=5),
            ])
        db.commit()
