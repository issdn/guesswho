from typing import Literal
from image_manipulation import get_random_image_names
from managers.base import SocketManager, task
from managers.player import Player


class Game(SocketManager):
    def __init__(self, players: list[Player], *args, **kwargs) -> None:
        super(Game, self).__init__(*args, **kwargs)
        self.players: list[Player] = players
        self.image_names: dict[Literal["names"], list[str]] = get_random_image_names()
        self.tasks = {
            "start": self.start_game,
        }

    @task
    def start_game(self, player: Player):
        pass
