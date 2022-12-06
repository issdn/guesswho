from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import secrets
from os.path import abspath
from phases_definitions import (
    LobbyPhase,
    PickCharacterPhase,
    GamePhase,
    PlayersJoinPhase,
    EndGamePhase,
)
from players_manager import Player
from queues import PhaseQueue

from models import Error, PlayerLeave

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

phase_queues: dict[str, PhaseQueue] = {}


@app.post("/newgame")
async def new_game():
    """
    1. Instances a PhaseQueue and saves it in phase_queues, where token is a key and instance is a value.
    2. Returns token for a new game.
    """
    token = secrets.token_urlsafe(8)
    phase_queues[token] = PhaseQueue(
        phases=(
            PlayersJoinPhase,
            LobbyPhase,
            PickCharacterPhase,
            GamePhase,
            EndGamePhase,
        )
    )
    return {"task": "init", "token": token}


@app.websocket("/{token}/game/ws")
async def game(token: str, websocket: WebSocket):
    """
    :: receive action
    -> handle action by type
    -> dispatch
    """
    phase_queue = phase_queues[token]

    await websocket.accept()
    if len(phase_queue.players_manager.players) >= 2:
        await phase_queue.send_error(Error("Lobby is full!"), websocket)
        return
    else:
        player = Player("anonymous", websocket)
    try:
        await phase_queue.player_loop(player)
    except WebSocketDisconnect:
        if not phase_queue.players_manager.players:
            del phase_queues[token]
        player_id = player.game_id
        phase_queue.players_manager.remove_player(player)
        phase_queue.reset_queue()
        for lobby_player in phase_queue.players_manager.players:
            await phase_queue.message_queue.send_task(
                lobby_player,
                PlayerLeave(
                    task="player_leave",
                    game_id=player_id,
                    new_creator_game_id=phase_queue.players_manager.get_new_creator().game_id,
                ),
            )
        phase_queue.message_queue.timed_tasks_delete_player_key(player_id)


@app.get("/{token}/characters")
async def game_data(token: str) -> dict[str, list[str]]:
    """
    List of names of characters generated by PlayersManager.get_random_image_names()
    """
    return {"names": phase_queues[token].players_manager.image_names}


@app.get("/{token}/characters/{image}")
async def image(token: str, image: str) -> (FileResponse | HTTPException):
    """
    Return url of an image from it's name.
    """
    return FileResponse(abspath("./characters/" + image + ".png"))
