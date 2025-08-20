from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import init_db, get_db
from .models import Player, Item

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    init_db()


def get_player(db: Session) -> Player:
    return db.get(Player, 1)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    player = get_player(db)
    items = db.query(Item).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "player": player, "items": items},
    )


@app.post("/attack", response_class=HTMLResponse)
def attack(request: Request, db: Session = Depends(get_db)):
    player = get_player(db)
    gold_gain = 10
    exp_gain = 20
    player.gold += gold_gain
    player.exp += exp_gain
    level_up_exp = player.level * 100
    if player.exp >= level_up_exp:
        player.exp -= level_up_exp
        player.level += 1
        player.hp += 10
        player.atk += 2
    db.commit()
    items = db.query(Item).all()
    return templates.TemplateResponse(
        "components/game.html",
        {
            "request": request,
            "player": player,
            "items": items,
            "message": f"Attacked monster! +{gold_gain} gold, +{exp_gain} exp.",
        },
    )


@app.post("/upgrade", response_class=HTMLResponse)
def upgrade(request: Request, db: Session = Depends(get_db)):
    player = get_player(db)
    cost = player.weapon_level * 50
    message = ""
    if player.gold >= cost:
        player.gold -= cost
        player.weapon_level += 1
        player.atk += 5
        db.commit()
        message = f"Upgraded weapon to level {player.weapon_level}!"
    else:
        message = "Not enough gold."
    items = db.query(Item).all()
    return templates.TemplateResponse(
        "components/game.html",
        {"request": request, "player": player, "items": items, "message": message},
    )


@app.post("/buy/{item_id}", response_class=HTMLResponse)
def buy_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    player = get_player(db)
    item = db.get(Item, item_id)
    message = ""
    if item and player.gold >= item.cost:
        player.gold -= item.cost
        player.atk += item.atk_bonus
        player.hp += item.hp_bonus
        db.commit()
        message = f"Purchased {item.name}!"
    else:
        message = "Cannot buy item."
    items = db.query(Item).all()
    return templates.TemplateResponse(
        "components/game.html",
        {"request": request, "player": player, "items": items, "message": message},
    )
