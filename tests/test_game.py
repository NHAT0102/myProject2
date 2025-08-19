import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app
from fastapi.testclient import TestClient
from app.database import SessionLocal, init_db
from app.models import Player

client = TestClient(app)


def setup_function(function):
    if os.path.exists("test.db"):
        os.remove("test.db")
    init_db()


def teardown_function(function):
    if os.path.exists("test.db"):
        os.remove("test.db")


def test_attack_increases_gold_and_exp():
    response = client.post("/attack")
    assert response.status_code == 200
    with SessionLocal() as db:
        player = db.get(Player, 1)
        assert player.gold == 10
        assert player.exp == 20
