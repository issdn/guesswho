import asyncio
from fastapi import WebSocket
from pydantic import ValidationError
from models import (
    PlayerJoinResponse,
    Task,
)
from collections import deque
from errors import CriticalServerException, ServerException
from models import Error
from players_manager import PlayersManager


class Timer:
    def __init__(
        self,
        delete_timed_task,
        timeout,
        player_game_id,
        overtime_callback,
        ending_task_name,
        additional_params,
    ):
        self._delete_timed_tasks = delete_timed_task
        self._timeout = timeout
        self._player_game_id = player_game_id
        self._overtime_callback = overtime_callback
        self._ending_task_name = ending_task_name
        self._additional_params = additional_params
        self._task = asyncio.create_task(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._overtime_callback(*self._additional_params)
        self._delete_timed_tasks(self._player_game_id, self._ending_task_name)

    def stop(self):
        self._task.cancel()
        self._delete_timed_tasks(self._player_game_id, self._ending_task_name)


class MessageQueue:
    def __init__(self, players) -> None:
        self.players = players
        self.timed_tasks = {}

    def add_timed_task(
        self,
        player_game_id,
        time,
        ending_task_name,
        overtime_callback,
        additional_params=(),
    ) -> None:
        timer = Timer(
            delete_timed_task=self.delete_timed_task,
            timeout=time,
            player_game_id=player_game_id,
            overtime_callback=overtime_callback,
            ending_task_name=ending_task_name,
            additional_params=additional_params,
        )
        self.timed_tasks[player_game_id][ending_task_name] = timer

    async def send_message(self, send_function_type, task=None, player=None) -> None:
        if send_function_type == 0:
            await self._send_task_to_all(task)
        elif send_function_type == 1:
            await self._send_task_to_enemy(player, task)
        elif send_function_type == 2:
            await self.send_task(player, task)
        elif send_function_type == 3:
            await self._send_init()

    def timed_tasks_allocate_player_key(self, player_game_id: int) -> None:
        self.timed_tasks[player_game_id] = {}

    async def send_task(self, player, task: Task) -> None:
        await player.websocket.send_json(task.json())

    async def _send_task_to_enemy(self, player, task) -> None:
        for game_player in self.players:
            if game_player != player:
                await game_player.websocket.send_json(task.json())

    async def _send_task_to_all(self, task) -> None:
        for game_player in self.players:
            await game_player.websocket.send_json(task.json())

    async def _send_init(self) -> None:
        for lobby_player in self.players:
            pjr = PlayerJoinResponse(
                task="player_join",
                game_id=lobby_player.game_id,
                players=[p.get_init_info() for p in self.players],
            )
            await lobby_player.websocket.send_json(pjr.json())

    def delete_timed_task(self, player_game_id: int, task_name: str) -> None:
        del self.timed_tasks[player_game_id][task_name]


class PhaseQueue:
    def __init__(self, phases) -> None:
        self._phases = phases
        self.players_manager = PlayersManager()
        self._queue = deque(self._phases)
        self.message_queue = MessageQueue(self.players_manager.players)
        self._set_phase_queue_index_null()

    def _shift_phases(self) -> None:
        self._queue.popleft()
        self._set_phase_queue_index_null()

    def _set_phase_queue_index_null(self) -> None:
        self._current_phase = self._queue[0](
            self.players_manager, self.message_queue, self._shift_phases
        )

    def reset_queue(self, start_index=1) -> None:
        self._queue = deque(self._phases[start_index:])
        self._set_phase_queue_index_null()

    async def player_loop(self, player) -> None:
        try:
            while True:
                message = await player.websocket.receive_json()
                task = self._current_phase.validator(**message)
                task_name = task.task
                task_function, send_function_type = self._current_phase.tasks[task_name]
                await task_function(player=player, task=task)
                if task_name in self.message_queue.timed_tasks[player.game_id]:
                    self.message_queue.timed_tasks[player.game_id][task_name].stop()
                await self.message_queue.send_message(send_function_type, task, player)
        except (ValidationError, ServerException) as e:
            await self._send_error(e, player.websocket)

    async def _send_error(
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
