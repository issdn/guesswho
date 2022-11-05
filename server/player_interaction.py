import json
from typing import Literal
from fastapi import WebSocket
from pydantic import ValidationError
from starlette.datastructures import Address
from models import PlayerInitInfo, PlayerJoin, PlayerJoinResponse, Task, Error, TaskType
from image_manipulation import get_random_image_names


async def send_error(message: str | list[ValidationError], websocket: WebSocket):
    if isinstance(message, ValidationError):
        for error in message.errors():
            print(error["loc"])
            validated_error = Error(
                type="error", message=error["msg"], field=error["loc"][0]
            )
            print(validated_error.json())
            await websocket.send_json(validated_error.json())
    else:
        validated_error = Error(type="error", message=message)
        await websocket.send_json(validated_error.json())


def validate_task(message: object):
    return Task(**message)


class Player:
    def __init__(self, nickname: str, websocket: WebSocket):
        self.nickname: str = nickname
        self.websocket: WebSocket = websocket
        self.address: Address = websocket.client
        self.lobby_id: int = None
        self.creator: bool = False
        self.ready: bool = False

    def switch_ready(self):
        self.ready = not self.ready

    def switch_creator(self):
        self.creator = not self.creator

    def set_nickname(self, nickname: str):
        self.nickname = nickname

    def get_init_info(self):
        return PlayerInitInfo(
            nickname=self.nickname,
            creator=self.creator,
            ready=self.ready,
            lobby_id=self.lobby_id,
        )

    def get_task(self, task_type: TaskType) -> Task:
        return Task(task=task_type, lobby_id=self.lobby_id).json()


class SocketManager:
    def __init__(self) -> None:
        self.players: list[Player] = None
        if self.players == None:
            self.players = []
        self.image_names = get_random_image_names()

    async def player_join(self, player: Player) -> None:
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.lobby_id == None:
            player.lobby_id = len(self.players) - 1
        await self.broadcast_init(player)

    def player_leave(self, player: Player) -> None:
        self.players.remove(player)

    async def broadcast(self, task: Task) -> None:
        for lobby_player in self.players:
            await lobby_player.websocket.send_json(task.json())

    async def broadcast_init(self, player: Player) -> None:
        for lobby_player in self.players:
            pjr = PlayerJoinResponse(
                task="player_join",
                lobby_id=lobby_player.lobby_id,
                players=[p.get_init_info() for p in self.players],
            )
            await lobby_player.websocket.send_json(pjr.json())


async def handle_player_join(
    message: object, lobby: SocketManager, websocket: WebSocket
) -> Player:
    try:
        task = PlayerJoin(**message)
        player = Player(task.nickname, websocket)
        await lobby.player_join(player)
        return player
    except ValidationError as e:
        await send_error(e, websocket)


async def start_game(lobby: SocketManager, player: Player):
    for lobby_player in lobby.players:
        if not lobby_player.ready:
            await send_error("Not all players ready!", player.websocket)
            return
    if not player.creator:
        await send_error("Game can only be started by the creator.", player.websocket)
        return
    await lobby.broadcast(Task(task="start"))


async def handle_task(message: object, lobby: SocketManager, player: Player) -> None:
    try:
        task = validate_task(message)
        print(task)
        task_type = task.task
        if task_type == "player_ready":
            player.switch_ready()
            await lobby.broadcast(task)
        elif task_type == "player_leave":
            lobby.player_leave(player)
            await lobby.broadcast(task)
        elif task_type == "set_creator":
            for lobby_player in lobby.players:
                lobby_player.switch_creator()
            await lobby.broadcast()
        elif task_type == "start":
            await start_game(lobby, player)
        else:
            await send_error("Incorrect task.", player.websocket)
    except ValidationError as e:
        await send_error(e, player.websocket)
