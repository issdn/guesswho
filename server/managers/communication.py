from asyncio import Task
from managers.player import Player
from models import PlayerJoinResponse


class Broadcast:
    async def all(task: Task, player: Player, players: list[Player]) -> None:
        for lobby_player in players:
            await lobby_player.websocket.send_json(task.json())

    async def enemy(task: Task, player: Player, players: list[Player]) -> None:
        for lobby_player in players:
            if lobby_player != player:
                await lobby_player.websocket.send_json(task.json())

    async def player(task: Task, player: Player, players: list[Player]) -> None:
        await player.websocket.send_json(task.json())

    async def init(player: Player, task: Task, players: list[Player]) -> None:
        for lobby_player in players:
            pjr = PlayerJoinResponse(
                task="player_join",
                game_id=lobby_player.game_id,
                players=[p.get_init_info() for p in players],
            )
            await lobby_player.websocket.send_json(pjr.json())

    async def bare_all(message: object, players: list[Player]):
        for lobby_player in players:
            await lobby_player.websocket.send_json(message)

    methods = (
        all,
        enemy,
        player,
        init,
    )
