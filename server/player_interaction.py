from argparse import Action
from fastapi import WebSocket
from pydantic import ValidationError
from starlette.datastructures import Address
from models import Info, Task, Error


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


class SocketManager:
    def __init__(self) -> None:
        self.players: list[Player] = None
        if self.players == None:
            self.players = []

    async def player_join(self, player: Player):
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.lobby_id == None:
            player.lobby_id = len(self.players)
        info = Info(
            type="info",
            task="player_join",
            nickname=player.nickname,
            creator=player.creator,
            lobby_id=player.lobby_id,
        )
        await self.broadcast(info)

    def player_leave(self, player: Player):
        self.players.remove(player.lobby_id)

    async def broadcast_info_omit_player(self, player: Player, action: Info | Action):
        for lobby_player in self.players:
            if player != lobby_player:
                await player.websocket.send_json(action.json())

    async def broadcast(self, action: Info | Action):
        for player in self.players:
            await player.websocket.send_json(action.json())


async def handle_task(message: object, lobby: SocketManager, player: Player):
    try:
        task = validate_task(message).task
        print(task)
        if task == "player_ready":
            player.switch_ready()
            print(player.ready)
        elif task == "player_leave":
            lobby.player_leave(player)
        elif task == "player_join":
            lobby.player_join(player)
        elif task == "set_creator":
            for lobby_player in lobby.players:
                lobby_player.switch_creator()
        else:
            await send_error("Incorrect task.", player.websocket)
    except ValidationError as e:
        await send_error(e, player.websocket)
