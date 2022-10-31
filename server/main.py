from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import secrets
from pydantic import ValidationError

from player_interaction import (
    SocketManager,
    Player,
    handle_task,
    send_error,
    handle_player_join,
)
from models import Info, Task

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lobbies: dict[str, SocketManager] = {}


@app.post("/newgame")
async def new_game():
    token = secrets.token_urlsafe(8)
    lobbies[token] = SocketManager()
    return {"type": "info", "token": token}


"""
- ACTION TYPES - 

task  :: always sent by user -> validated by server -> sent to all users
error :: always sent by server to a single user
info  :: sent by user or server
"""


@app.websocket("/{token}/lobby/ws")
async def game(token: str, websocket: WebSocket):
    """
    :: receive action
    -> handle action by type
    -> dispatch
    """
    lobby = lobbies[token]

    await websocket.accept()
    if len(lobby.players) < 2:
        initial_data = await websocket.receive_json()
        player = await handle_player_join(initial_data, lobby, websocket)

        while True:
            message = await websocket.receive_json()
            await handle_task(message, lobby, player)
    else:
        await send_error("Lobby is full.", websocket)
        websocket.close(code=1007)


@app.websocket("/{token}/game/ws")
async def game(token: str, websocket: WebSocket):
    lobby = lobbies[token]
    while True:
        data = await websocket.receive_json()
        await lobby.broadcast(data)
