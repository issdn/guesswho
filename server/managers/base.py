from fastapi import WebSocket
from pydantic import ValidationError
from models import (
    Task,
    Error,
)
from managers.player import Player


async def send_error(message: list[ValidationError] | Error, websocket: WebSocket):
    if isinstance(message, ValidationError):
        for error in message.errors():
            validated_error = Error(
                type="error", message=error["msg"], field=error["loc"][0]
            )
            await websocket.send_json(validated_error.json())
        websocket.close()
    elif isinstance(message, Error):
        await websocket.send_json(message.json())
        websocket.close()


def task(func: callable) -> None:
    async def wrapper(*args, **kwargs):
        result = func(self=kwargs["self"], player=kwargs["player"])
        if not result:
            await kwargs["self"].broadcast(kwargs["task"])
        else:
            return result

    return wrapper


def validate(func: callable) -> None:
    async def wrapper(*args, **kwargs) -> callable:
        result = func()
        if isinstance(result, Error) or isinstance(result, ValidationError):
            await send_error(result, kwargs["player"].websocket)

    return wrapper


class SocketManager:
    def __init__(self) -> None:
        self.open = False
        self.players: list[Player] = None
        if self.players == None:
            self.players = []

        self.tasks = {}

    def set_open(self, value: bool):
        self.open = value

    async def main_loop(self, player: Player) -> None:
        self.open = True
        while self.open:
            message = await player.websocket.receive_json()
            await self.handle_task(message, player)

    def player_leave(self, player: Player) -> None:
        self.players.remove(player)

    async def broadcast(self, task: Task) -> None:
        for lobby_player in self.players:
            await lobby_player.websocket.send_json(task.json())

    async def handle_task(self, message: object, player: Player) -> None:
        try:
            task = Task(**message)
            task_type = task.task
            await self.tasks[task_type](self=self, player=player, task=task)
        except ValidationError as e:
            await send_error(e, player.websocket)
