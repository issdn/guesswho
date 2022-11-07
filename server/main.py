from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import secrets
from os.path import abspath

from managers.lobby import Lobby

from models import Task
from managers.game import Game

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lobbies: dict[str, Lobby] = {}
games: dict[str, Game] = {}


@app.post("/newgame")
async def new_game():
    token = secrets.token_urlsafe(8)
    lobbies[token] = Lobby()
    return {"task": "init", "token": token}


"""
- ACTION TYPES - 

task  :: always sent by user -> validated by server -> sent to all users
error :: always sent by server to a single user
"""


@app.websocket("/{token}/lobby/ws")
async def lobby(token: str, websocket: WebSocket):
    """
    :: receive action
    -> handle action by type
    -> dispatch
    """
    lobby = lobbies[token]

    await websocket.accept()
    try:
        initial_data = await websocket.receive_json()
        player = await lobby.handle_player_join(initial_data, websocket)
        await lobby.main_loop(player)
        game = Game(lobby.players)
        games[token] = game
        await game.main_loop(player)
    except WebSocketDisconnect:
        player_id = player.lobby_id
        lobby.player_leave(player)
        await lobby.broadcast(Task(task="player_leave", lobby_id=player_id))


@app.get("/{token}/characters")
async def game_data(token: str):
    return games[token].image_names


@app.get("/{token}/characters/{image}")
async def image(token: str, image: str):
    try:
        if image in games[token].image_names["names"]:
            return FileResponse(abspath("./characters/" + image + ".png"))
    except KeyError:
        return HTTPException(404, "Image with this name doesn't exist.")
