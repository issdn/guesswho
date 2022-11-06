from fastapi import WebSocket
from pydantic import ValidationError
from starlette.datastructures import Address
from models import PlayerInitInfo, PlayerJoin, PlayerJoinResponse, Task, Error, TaskType
from image_manipulation import get_random_image_names


async def send_error(
    message: str | list[ValidationError] | Error, websocket: WebSocket
):
    if isinstance(message, ValidationError):
        for error in message.errors():
            validated_error = Error(
                type="error", message=error["msg"], field=error["loc"][0]
            )
            await websocket.send_json(validated_error.json())
    elif isinstance(message, Error):
        await websocket.send_json(message.json())
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


def task(func: callable) -> None:
    async def wrapper(*args, **kwargs):
        result = func(self=kwargs["self"], player=kwargs["player"])
        if isinstance(result, Error):
            await send_error(result, kwargs["player"].websocket)
        elif not result:
            await kwargs["self"].broadcast(kwargs["task"])

    return wrapper


class SocketManager:
    def __init__(self) -> None:
        self.players: list[Player] = None
        if self.players == None:
            self.players = []

        self.tasks = {}

    def player_leave(self, player: Player) -> None:
        self.players.remove(player)

    async def broadcast(self, task: Task) -> None:
        for lobby_player in self.players:
            await lobby_player.websocket.send_json(task.json())

    async def handle_task(self, message: object, player: Player) -> None:
        try:
            task = validate_task(message)
            task_type = task.task
            await self.tasks[task_type](self=self, player=player, task=task)
        except ValidationError as e:
            await send_error(e, player.websocket)


class Lobby(SocketManager):
    def __init__(self, *args, **kwargs) -> None:
        super(Lobby, self).__init__(*args, **kwargs)

        self.tasks = {
            "player_ready": self.player_ready,
            "player_leave": self.player_leave,
            "start": self.start_game,
        }

    async def player_join(self, player: Player) -> None:
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.lobby_id == None:
            player.lobby_id = len(self.players) - 1
        await self.broadcast_init()

    async def broadcast_init(self) -> None:
        for lobby_player in self.players:
            pjr = PlayerJoinResponse(
                task="player_join",
                lobby_id=lobby_player.lobby_id,
                players=[p.get_init_info() for p in self.players],
            )
            await lobby_player.websocket.send_json(pjr.json())

    async def handle_player_join(self, message: object, websocket: WebSocket) -> Player:
        try:
            task = PlayerJoin(**message)
            player = Player(task.nickname, websocket)
            await self.player_join(player)
            return player
        except ValidationError as e:
            await send_error(e, websocket)

    @task
    def start_game(self, player: Player):
        for lobby_player in self.players:
            if not lobby_player.ready:
                return Error(message="Not all players ready!")
        if not player.creator:
            return Error(message="Game can only be started by the creator.")

    @task
    def player_ready(self, player: Player) -> None:
        player.switch_ready()

    @task
    def player_leave(self, player: Player) -> None:
        self.player_leave(player)


class Game(SocketManager):
    def __init__(self, *args, **kwargs) -> None:
        super(Game, self).__init__(*args, **kwargs)
        self.image_names = get_random_image_names()
