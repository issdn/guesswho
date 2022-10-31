from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import secrets

from player_interaction import (
    SocketManager,
    handle_task,
    send_error,
    handle_player_join,
)

from models import Task

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
    try:
        if len(lobby.players) < 2:
            initial_data = await websocket.receive_json()
            player = await handle_player_join(initial_data, lobby, websocket)

            while True:
                message = await websocket.receive_json()
                await handle_task(message, lobby, player)
        else:
            await send_error("Lobby is full.", websocket)
            await websocket.close(code=1007)
    except WebSocketDisconnect:
        player_id = player.lobby_id
        lobby.player_leave(player)
        await lobby.broadcast(Task(task="player_leave", lobby_id=player_id))
