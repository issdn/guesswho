from pydantic import ValidationError
from managers.base import SocketManager, send_error, task, validate
from managers.player import Player
from models import Error, PlayerJoin, PlayerJoinResponse
from fastapi import WebSocket


class Lobby(SocketManager):
    def __init__(self, *args, **kwargs) -> None:
        super(Lobby, self).__init__(*args, **kwargs)

        self.tasks = {
            "player_join": self.player_join,
            "player_ready": self.player_ready,
            "player_leave": self.player_leave,
            "start": self.start_game,
        }

    async def player_join(self, player: Player) -> None:
        if len(self.players) == 0:
            player.switch_creator()
        self.players.append(player)
        if player.lobby_id == None:
            player.lobby_id = self.players.index(player)
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
        if len(self.players) < 2:
            try:
                task = PlayerJoin(**message)
                player = Player(task.nickname, websocket)
                await self.player_join(player)
                return player
            except ValidationError as e:
                send_error(e)
        else:
            send_error(Error(message="Lobby is full."))

    @task
    def start_game(self, player: Player):
        self.check_player_creator(player)
        self.check_players_ready()
        self.open = False

    @task
    def player_ready(self, player: Player) -> None:
        player.switch_ready()

    @task
    def player_leave(self, player: Player) -> None:
        self.player_leave(player)

    @validate
    def check_player_creator(self, player: Player):
        if not player.creator:
            return Error(message="Game can only be started by the creator.")

    @validate
    def check_players_ready(self):
        for lobby_player in self.players:
            if not lobby_player.ready:
                return Error(message="Not all players ready!")
