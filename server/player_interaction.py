import json
from typing import Literal
from fastapi import WebSocket
from pydantic import ValidationError
from starlette.datastructures import Address
from models import PlayerInitInfo, PlayerJoin, Task, Error, TaskType


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
        )

    def get_task(self, task_type: TaskType) -> Task:
        return Task(task=task_type, lobby_id=self.lobby_id).json()


class SocketManager:
    def __init__(self) -> None:
        self.players: list[Player] = None
        if self.players == None:
            self.players = []

    def get_every_player_status(
        self, player: Player
    ) -> dict[Literal["player", "enemy"], object]:
        return {
            "player" if p == player else "enemy": p.get_info().dict()
            for p in self.players
        }

    async def player_join(self, player: Player) -> None:
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.lobby_id == None:
            player.lobby_id = len(self.players) - 1
        await self.broadcast_init(player)

    def player_leave(self, player: Player):
        self.players.remove(player)

    async def broadcast(self, task: Task):
        for lobby_player in self.players:
            await lobby_player.websocket.send_json(task.json())

    async def broadcast_init(self, player: Player) -> None:
        players_in_lobby = {"player_id": player.lobby_id, "task": "player_join"}
        for p in self.players:
            players_in_lobby[p.lobby_id] = p.get_init_info().dict()

        for lobby_player in self.players:
            await lobby_player.websocket.send_json(json.dumps(players_in_lobby))


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


async def handle_task(message: object, lobby: SocketManager, player: Player) -> None:
    try:
        task = validate_task(message)
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
        else:
            await send_error("Incorrect task.", player.websocket)
    except ValidationError as e:
        await send_error(e, player.websocket)
