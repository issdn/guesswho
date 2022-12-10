import asyncio
from errors import CriticalServerException
from models import BaseTaskModel, PlayerJoinResponseModel


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

    async def send_task(self, player, task: BaseTaskModel) -> None:
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
            pjr = PlayerJoinResponseModel(
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
        for task in _to_stop:
            task.stop()