from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import secrets
from pydantic import ValidationError

from player_interaction import (
    SocketManager,
    Player,
    handle_task,
    send_error,
    validate_action,
)

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
    return {"init": {"token": token}}


"""
- ACTION TYPES - 

task  :: always sent by user -> validated by server -> sent to all users
error :: always sent by server to a single user
init  :: always sent by single user to server
info  :: always sent by server to minimum 1 user
"""


@app.websocket("/{token}/lobby/ws")
async def game(token: str, websocket: WebSocket):
    """
    :: receive action
    -> handle action by type
    -> dispatch
    """
    lobby = lobbies[token]

    if len(lobby.players) < 2:
        await websocket.accept()

        try:
            initial_data = await websocket.receive_json()
            initial_data = validate_action(initial_data)
        except ValidationError as e:
            await send_error(e.json(), websocket)
            await websocket.close(code=1007)
            return

        p = Player(initial_data.data["nickname"], websocket)
        await lobby.player_join(p)

        while True:
            message = await p.websocket.receive_json()
            await handle_task(message, lobby, p)
    else:
        await send_error("Lobby is full.", websocket)


@app.websocket("/{token}/game/ws")
async def game(token: str, websocket: WebSocket):
    lobby = lobbies[token]
    while True:
        data = await websocket.receive_json()
        await lobby.broadcast(data)
