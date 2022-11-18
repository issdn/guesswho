from fastapi import WebSocket
from starlette.datastructures import Address

from models import PlayerInitInfo, Task, TaskType
from errors import ServerException


class Player:
    def __init__(self, nickname: str, websocket: WebSocket):
        self.nickname: str = nickname
        self.websocket: WebSocket = websocket
        self.address: Address = websocket.client
        self.game_id: int = None
        self.creator: bool = False
        self.ready: bool = False
        self.character: str = None

    def set_nickname(self, nickname: str):
        self.nickname = nickname

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
            game_id=self.game_id,
        )

    def get_task(self, task_type: TaskType) -> Task:
        return Task(task=task_type, game_id=self.game_id).json()


class PlayersManager:
    def __init__(self) -> None:
        self.players: list[Player] = []

    def remove_player(self, player: Player) -> None:
        self.players.remove(player)

    def add_player(self, player: Player) -> None:
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.game_id == None:
            player.game_id = self.players.index(player)

    def can_start_game(self, player: Player) -> None:
        if not player.creator:
            raise ServerException("Game can only be started by the creator.")
        for lobby_player in self.players:
            if not lobby_player.ready:
                raise ServerException("Not all players ready!")
