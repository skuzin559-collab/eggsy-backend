from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uuid

app = FastAPI()

# Временное хранилище игроков (потом заменим на БД)
players: Dict[str, dict] = {}

class PlayerCreate(BaseModel):
    nickname: str

class PlayerUpdate(BaseModel):
    coins: int


@app.get("/")
def root():
    return {"message": "Eggsy сервер работает 🚀"}


# 🔹 Регистрация игрока
@app.post("/register")
def register(player: PlayerCreate):
    player_id = str(uuid.uuid4())

    players[player_id] = {
        "nickname": player.nickname,
        "coins": 0
    }

    return {"player_id": player_id}


# 🔹 Получить данные игрока
@app.get("/player/{player_id}")
def get_player(player_id: str):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Игрок не найден")

    return players[player_id]


# 🔹 Обновить монеты
@app.post("/player/{player_id}/update")
def update_player(player_id: str, data: PlayerUpdate):
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Игрок не найден")

    players[player_id]["coins"] = data.coins
    return {"status": "updated"}
