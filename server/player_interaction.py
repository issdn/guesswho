from typing import Literal
from fastapi import WebSocket
from pydantic import ValidationError
from starlette.datastructures import Address
from models import Info, InfoBase, Task, Error, TaskType
import json


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

    def get_info(self):
        return InfoBase(
            nickname=self.nickname,
            lobby_id=self.lobby_id,
            creator=self.creator,
            ready=self.ready,
        )

    def create_info(self, task_type: str) -> Info:
        return Info(type="info", task=task_type, **self.get_info().dict())

class SocketManager:
    def __init__(self) -> None:
        self.players: list[Player] = None
        if self.players == None:
            self.players = []

    def get_every_player_status(self, player: Player) -> dict[Literal["player","enemy"], object]:
        return {"player" if p == player else "enemy": p.get_info().dict() for p in self.players}

    def get_player_status(self, player: Literal["player", "enemy"]):
        if player == "player":
            for p in self.players:
                if p == player:
                    return p.get_info().dict()
        elif player == "enemy":
            for p in self.players:
                if p != player:
                    return p.get_info().dict()
        else:
            Exception("Incorrect player tag: Must be either 'player' or 'enemy'.")

    async def player_join(self, player: Player) -> None:
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.lobby_id == None:
            player.lobby_id = len(self.players)
        players_dict = self.get_every_player_status(player)
        await self.broadcast_task_by_player_type(players_dict)

    def player_leave(self, player: Player):
        self.players.remove(player.lobby_id)

    async def broadcast_info_omit_player(self, player: Player, task: Info | Task) -> None:
        for lobby_player in self.players:
            if player != lobby_player:
                await player.websocket.send_json(task.json())

    async def broadcast_task(self, task: Info | Task | list | dict) -> None:
        if isinstance(task, list) or isinstance(task, dict):
            for player in self.players:
                await player.websocket.send_json(json.dumps(task))
        elif isinstance(task, Task):
            for player in self.players:
                await player.websocket.send_json(task.json())

    async def broadcast_task_by_player_type(self, task: Task, task_type: TaskType, player: Player) -> None:
        message = {"task": task_type}
        for lobby_player in self.players:
            if lobby_player == player:
                message["player"] = task.dict() 
                await lobby_player.websocket.send_json(json.dump(message))
            elif lobby_player != player:
                message["enemy"] = task.dict() 
                await lobby_player.websocket.send_json(json.dump(message))


async def handle_player_join(
    message: object, lobby: SocketManager, websocket: WebSocket
) -> Player:
    try:
        task = validate_task(message)
        player = Player(task.nickname, websocket)
        player.set_nickname(task.nickname)
        await lobby.player_join(player)
        return player
    except ValidationError as e:
        await send_error(e, websocket)
        websocket.close(code=1007)


async def handle_task(message: object, lobby: SocketManager, player: Player) -> None:
    try:
        task = validate_task(message)
        task_type = task.task
        if task_type == "player_ready":
            player.switch_ready()
            await lobby.broadcast_task(player.create_info(task.task))
        elif task_type == "player_leave":
            lobby.player_leave(player)
            lobby.get_player_status("")
            await lobby.broadcast_task(player.create_info(task.task))
        elif task_type == "set_creator":
            for lobby_player in lobby.players:
                lobby_player.switch_creator()
                await lobby.broadcast_task(lobby_player.create_info(task.task))
        else:
            await send_error("Incorrect task.", player.websocket)
    except ValidationError as e:
        await send_error(e, player.websocket)
