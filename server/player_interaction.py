from fastapi import WebSocket
from pydantic import ValidationError
from starlette.datastructures import Address
from models import Info, Init, Task, Action, Error, action_types


async def send_error(message: str | ValidationError, websocket: WebSocket):
    if isinstance(message, ValidationError) or isinstance(message, dict):
        await websocket.send_json({"type": "error", "data": message})
    else:
        error = Error(message=message)
        await websocket.send_json({"type": "error", "data": error.json()})


def validate_action(message: object) -> Action:
    a = Action(**message)
    action_types[a.type](**a.data)
    return a


def validate_task(message: object):
    a = Action(**message)
    return Task(a.data)


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
            task="player_join",
            nickname=player.nickname,
            creator=player.creator,
            lobby_id=player.lobby_id,
        )
        print(info.dict())
        action = Action(type="info", data=info.dict())
        await self.broadcast(action)

    def player_leave(self, player: Player):
        self.players.remove(player.lobby_id)

    async def broadcast_info_omit_player(self, player: Player, action: str):
        for lobby_player in self.players:
            if player != lobby_player:
                await player.websocket.send_json(action.json())

    async def broadcast(self, action: Action):
        for player in self.players:
            await player.websocket.send_json(action.json())


async def handle_task(message: object, lobby: SocketManager, player: Player):
    try:
        task = message
        if task == "player_ready":
            player.switch_ready()
        elif task == "player_leave":
            lobby.player_leave(player)
        elif task == "player_join":
            lobby.player_join(player)
        elif task == "set_creator":
            for lobby_player in lobby.players:
                lobby_player.switch_creator()
        else:
            err = Error("Oops, something went wrong!")
            await send_error(err, player.websocket)
    except ValidationError as e:
        await send_error(e.json(), player.websocket)
