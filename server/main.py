from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import secrets
from os.path import abspath
from managers.phases import LobbyPhase, GamePrepPhase, GamePhase, PlayersJoinPhase
from managers.player import Player
from managers.game import Game

from models import Error, Task

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

games: dict[str, Game] = {}


@app.post("/newgame")
async def new_game():
    token = secrets.token_urlsafe(8)
    games[token] = Game(phases=(PlayersJoinPhase, LobbyPhase, GamePrepPhase, GamePhase))
    return {"task": "init", "token": token}


"""
- ACTION TYPES - 

task  :: always sent by user -> validated by server -> sent to all users
error :: always sent by server to a single user
"""


@app.websocket("/{token}/game/ws")
async def game(token: str, websocket: WebSocket):
    """
    :: receive action
    -> handle action by type
    -> dispatch
    """
    game = games[token]

    await websocket.accept()
    if len(game.players_manager.players) >= 2:
        await game.send_error(Error("Lobby is full!"), websocket)
        return
    else:
        player = Player("anonymous", websocket)

    try:
        await game.player_loop(player)
    except WebSocketDisconnect:
        player_id = player.game_id
        game.players_manager.remove_player(player)
        game.back_to_lobby()
        await game.broadcast(Task(task="player_leave", game_id=player_id))


@app.get("/{token}/characters")
async def game_data(token: str):
    return games[token].players_manager.image_names


@app.get("/{token}/characters/{image}")
async def image(token: str, image: str):
    try:
        if image in games[token].players_manager.image_names["names"]:
            return FileResponse(abspath("./characters/" + image + ".png"))
    except KeyError:
        return HTTPException(404, "Image with this name doesn't exist.")


@app.get("/{token}/starting_player")
async def starting_player(token: str):
    print(games[token].players_manager.currently_asking_player)
    return {"starting_player_id": games[token].players_manager.currently_asking_player}
