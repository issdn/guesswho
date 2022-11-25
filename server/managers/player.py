import random
from typing import Literal
from fastapi import WebSocket
from starlette.datastructures import Address

from models import PlayerInitInfo, Task, TaskTypes
from errors import ServerException
from image_manipulation import get_random_image_names


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

    def set_character(self, character_name: str):
        self.character = character_name

    def get_init_info(self):
        return PlayerInitInfo(
            nickname=self.nickname,
            creator=self.creator,
            ready=self.ready,
            game_id=self.game_id,
        )

    def get_task(self, task_type: TaskTypes) -> Task:
        return Task(task=task_type, game_id=self.game_id).json()


class PlayersManager:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.image_names: dict[Literal["names"], list[str]] = get_random_image_names()
        self.currently_asking_player = None

    def change_currently_asking_player(self):
        for lobby_player in self.players:
            if lobby_player.game_id != self.currently_asking_player:
                self.currently_asking_player = lobby_player.game_id
                return

    def get_enemy(self, player: Player) -> Player:
        for lobby_player in self.players:
            if player != lobby_player:
                return lobby_player

    def draw_starting_player(self):
        self.currently_asking_player = random.choice(self.players).game_id

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

    def all_playes_characters_picked(self) -> bool:
        for lobby_player in self.players:
            if not lobby_player.character:
                return False
        return True
