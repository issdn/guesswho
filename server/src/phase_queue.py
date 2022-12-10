from fastapi import WebSocket
from pydantic import ValidationError
from collections import deque
from errors import CriticalServerException, ServerException
from message_manager import MessageManager
from models import ErrorModel
from players_manager import PlayersManager

class PhaseQueue:
    def __init__(self, phases) -> None:
        self._phases = phases
        self.players_manager = PlayersManager()
        self._queue = deque(self._phases)
        self.message_queue = MessageManager(self.players_manager.players)
        self._set_phase_queue_index_null()

    def _shift_phases(self) -> None:
        self.message_queue.delete_all_timed_tasks()
        self._queue.popleft()
        self._set_phase_queue_index_null()

    def _set_phase_queue_index_null(self) -> None:
        self._current_phase = self._queue[0](
            self.players_manager, self.message_queue, self._shift_phases, self.reset_queue
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
                print(message)
                task = self._current_phase.validator(**message)
                task_name = task.task
                task_function, send_function_type = self._current_phase.tasks[task_name]
                await task_function(player=player, task=task)
                if task_name in self.message_queue.timed_tasks[player.game_id]:
                    self.message_queue.timed_tasks[player.game_id][task_name].stop()
                await self.message_queue.send_message(send_function_type, task, player)
            except (ValidationError, ServerException) as e:
                await self._send_error(e, player.websocket)

    async def send_error(
        self,
        error: list[ValidationError] | ErrorModel | ServerException,
        websocket: WebSocket,
    ):
        if isinstance(error, ValidationError):
            for error in error.errors():
                validated_error = ErrorModel(
                    type="error", message=error["msg"], field=error["loc"][0]
                )
                await websocket.send_json(validated_error.json())
        elif isinstance(error, ServerException):
            validated_error = ErrorModel(message=error.message)
            await websocket.send_json(validated_error.json())
        elif isinstance(error, ErrorModel):
            await websocket.send_json(error.json())
        else:
            raise CriticalServerException(
                f"{error.__class__.__name__} is an invalid error object!"
            )
