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
        if not isinstance(self._additional_params, tuple):
            raise CriticalServerException("Additional params must be of type tuple.")
        self._task = asyncio.create_task(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._overtime_callback(*self._additional_params)
        self._delete_timed_tasks(self._player_game_id, self._ending_task_name)

    def stop(self):
        """Stops currently running task (As in ``asyncio.create_task``)."""
        self._task.cancel()
        self._delete_timed_tasks(self._player_game_id, self._ending_task_name)


class MessageManager:
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
        """Main function for sending messages.

        ``send_function_type``: number from 0 - 3, where the numbers mean:

        - [0]  send to all clients
        - [1]  send to all players except the one specified as the player parameter
        - [2]  send to player specified as parameter
        - [3]  send player init info to all players
        - [4]  don't send
        """
        if send_function_type == 4:
            return
        if send_function_type == 0:
            await self._send_task_to_all(task)
        elif send_function_type == 1:
            await self._send_task_to_enemy(player, task)
        elif send_function_type == 2:
            await self.send_task(player, task)
        elif send_function_type == 3:
            await self._send_init()

    def timed_tasks_allocate_player_key(self, player_game_id: int) -> None:
        """Creates an entry in timed_tasks dictionary with key of player's ``game_id`` and value of empty nested dictionary."""
        self.timed_tasks[player_game_id] = {}

    def timed_tasks_delete_player_key(self, player_game_id: int) -> None:
        """Delete an entry with specified ``player_game_id`` from ``timed_tasks`` dictionary."""
        del self.timed_tasks[player_game_id]

    async def send_task(self, player, task: Task) -> None:
        """Directly send task to the specified player."""
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
        """Deletes entry from ``timed_tasks[player_id]`` nested dictionary."""
        del self.timed_tasks[player_game_id][task_name]

    def delete_all_timed_tasks(self) -> None:
        """Deletes all currently running timed tasks from every players' dictionary."""
        _to_stop = []
        for player_task_list in self.timed_tasks.values():
            for timed_task in player_task_list.values():
                _to_stop.append(timed_task)
        (task.stop() for task in _to_stop)


class PhaseQueue:
    def __init__(self, phases) -> None:
        self._phases = phases
        self.players_manager = PlayersManager()
        self._queue = deque(self._phases)
        self.message_queue = MessageManager(self.players_manager.players)
        self._set_phase_queue_index_null()

    def _shift_phases(self) -> None:
        self._queue.popleft()
        self._set_phase_queue_index_null()

    def _set_phase_queue_index_null(self) -> None:
        self._current_phase = self._queue[0](
            self.players_manager, self.message_queue, self._shift_phases
        )

    def reset_queue(self, start_index=0) -> None:
        """Resets queue, sets index to 0 or specified, resets players_manager data and deletes all timed tasks."""
        self._queue = deque(self._phases[start_index:])
        self._set_phase_queue_index_null()
        self.players_manager.reset_all_game_data()
        self.message_queue.delete_all_timed_tasks()

    async def player_loop(self, player) -> None:
        """Main loop for client-server communication.

        In an infinite loop, it:
        1. Waits for a message from player.
        2. Validates the message with a validator specified in current phase.
        3. Calls the task's function specified in message.task.
        4. Checks if the task is supposed to end any timed task for the player. If is then stops it.
        5. Sends the message back to specified in it's phase class players.
        6. ERROR: Catches ValidationError from pydantic or ServerException from ./errors.
        """
        while True:
            try:
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
        elif isinstance(error, ServerException):
            validated_error = Error(message=error.message)
            await websocket.send_json(validated_error.json())
        else:
            raise CriticalServerException(
                f"{error.__class__.__name__} is an invalid error object!"
            )
