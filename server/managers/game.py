from random import choice
from typing import Literal
from fastapi import WebSocket
from pydantic import ValidationError
from managers.player import Player, PlayersManager
from models import (
    PlayerJoinResponse,
    Task,
)
from managers.phases import BasePhase
from errors import CriticalServerException, ServerException
from models import Error


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

    methods = (
        all,
        enemy,
        player,
        init,
    )


class Game:
    def __init__(self, phases: tuple[BasePhase]) -> None:
        self.players_manager: PlayersManager = PlayersManager()
        self.phases = tuple(
            [
                phase(self.players_manager, self.end_phase, self.back_to_lobby)
                for phase in phases
            ]
        )
        self.current_phase_position: int = 0

    def end_phase(self):
        self.current_phase_position += 1
        print(self.phases[self.current_phase_position])

    def back_to_lobby(self):
        self.current_phase_position = 0

    async def player_loop(self, player: Player):
        try:
            while True:
                message = await player.websocket.receive_json()
                await self._handle_message(message, player)
        except (ValidationError, ServerException) as e:
            await self.send_error(e, player.websocket)

    async def _handle_message(self, message: object, player: Player) -> None:
        try:
            phase = self.phases[self.current_phase_position]
            print(message)
            print(phase)
            print(phase.validator)
            task = phase.validator(**message)
            task_type = task.task
            phase.tasks[task_type][0](
                player=player,
                task=task,
            )
        except (ServerException, ValidationError) as e:
            raise e
        await Broadcast.methods[phase.tasks[task_type][1]](
            player=player, task=task, players=self.players_manager.players
        )

    async def send_error(
        self,
        error: list[ValidationError] | Error | ServerException,
        websocket: WebSocket,
    ):
        if isinstance(error, ValidationError):
            for error in error.errors():
                validated_error = Error(
                    type="error", message=error["msg"], field=error["loc"][0]
                )
                await websocket.send_json(validated_error.json())
            await websocket.close()
        elif isinstance(error, ServerException):
            validated_error = Error(message=error.message)
        elif isinstance(error, Error):
            await websocket.send_json(error.json())
            await websocket.close()
        else:
            raise CriticalServerException(
                f"{error.__class__.__name__} is an invalid error object!"
            )
