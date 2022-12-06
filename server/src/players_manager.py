import random
from fastapi import WebSocket
from starlette.datastructures import Address
from models import PlayerInitInfo
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

    def get_init_info(self) -> PlayerInitInfo:
        """Returns PlayerInitInfo
        - nickname
        - creator - whether the player is the lobby creator
        - ready - whether the player is ready
        - game_id
        """
        return PlayerInitInfo(
            nickname=self.nickname,
            creator=self.creator,
            ready=self.ready,
            game_id=self.game_id,
        )

    def reset_game_data(self) -> None:
        """Resets Player.ready and Player.character."""
        self.ready = False
        self.character = None


class PlayersManager:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.image_names: list[str] = get_random_image_names()
        self.currently_asking_player_game_id = None
        self.currently_answering_player_game_id = None

    def change_currently_asking_player_game_id(self):
        """Swaps ``currently_answering_player_game_id`` with ``currently_asking_player_game_id``."""
        currently_answering_player_temp = self.currently_answering_player_game_id
        self.currently_answering_player_game_id = self.currently_asking_player_game_id
        self.currently_asking_player_game_id = currently_answering_player_temp

    def get_enemy(self, player: Player) -> Player:
        """Returns a player that is not the player passed as the argument."""
        for lobby_player in self.players:
            if player != lobby_player:
                return lobby_player

    def draw_random_character_name(self) -> str:
        return random.choice(self.image_names)

    def draw_starting_player(self):
        """Picks random player, sets ``currently_asking_player_game_id`` to it's game_id and ``currently_answering_player_game_id`` to the other player's id in lobby."""
        random_player = random.choice(self.players)
        self.currently_asking_player_game_id = random_player.game_id
        self.currently_answering_player_game_id = self.get_enemy(random_player).game_id

    def remove_player(self, player: Player) -> None:
        self.players.remove(player)

    def add_player(self, player: Player) -> None:
        """Adds player to list, gives it an id and if the list was previously empty, sets player as creator."""
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.game_id == None:
            player.game_id = self.players.index(player)

    def can_start_game(self, player: Player) -> None:
        """Checks whether player sending start_game message is creator and wheteher all players are ready."""
        if not player.creator:
            raise ServerException("Game can only be started by the creator.")
        for lobby_player in self.players:
            if not lobby_player.ready:
                raise ServerException("Not all players ready!")

    def all_playes_characters_picked(self) -> bool:
        """Checks if all players have picked a character."""
        for lobby_player in self.players:
            if not lobby_player.character:
                return False
        return True

    def get_new_creator(self) -> Player:
        """Sets first player in the players list as creator."""
        self.players[0].creator = True
        return self.players[0]

    def reset_all_game_data(self) -> None:
        """Resets ``currently_asking_player_game_id``, ``currently_answering_player_game_id`` and calls ``Player.reset_game_data()``"""
        for game_player in self.players:
            game_player.reset_game_data()
        self.currently_asking_player_game_id = None
        self.currently_answering_player_game_id = None
