import asyncio
import random
from pydantic import ValidationError
from managers.player import Player
from models import (
    CharactersPicked,
    GameEnd,
    PlayerJoin,
    QuestionAsk,
    StartingCharacterPick,
    Task,
)
from errors import ServerException, errors_by_code


class TaskSequence:
    def __init__(self) -> None:
        self.tasks = []

    def add_task(self, name: str, task: callable, validator) -> None:
        pass

    def add_timed_task(
        self,
        name: str,
        task: callable,
        validator,
        overtime_callback: callable,
        time: int,
    ) -> None:
        pass


class TaskLoop(TaskSequence):
    def __init__(self) -> None:
        super().__init__()


class AsyncTaskLoop(TaskSequence):
    def __init__(self) -> None:
        super().__init__()


class TaskStack(TaskSequence):
    def __init__(self) -> None:
        super().__init__()

    def add_server_task(self, task: callable, task_model) -> None:
        pass

    def add_task_loop(self, task_loop: TaskLoop, loop_end_condition_task: callable):
        pass

    def add_async_task_loop(
        self, async_task_loop: AsyncTaskLoop, loop_end_condition_task: callable
    ):
        pass

    async def player_loop(self):
        try:
            while True:
                message = await player.websocket.receive_json()
                await self._handle_message(message, player)
        except (ValidationError, ServerException) as e:
            await self.send_error(e, player.websocket)


# joining and leaving lobby
def player_leave(self, player: Player, task: Task) -> None:
    self.players_manager.player_leave(player)
    self.back_to_lobby()


def player_join_3(self, player: Player, task: PlayerJoin) -> None:
    """
    Set player's nickname taken from the task, add player to players_manager<PlayersManager>.
    If the lobby is full (2 players), end the phase.
    """
    player.set_nickname(task.nickname)
    self.players_manager.add_player(player)
    if len(self.players_manager.players) == 2:
        self.end_phase()


# being ready & starting the game
def player_ready(self, player: Player, task: Task) -> None:
    player.switch_ready()


def start_game(self, player: Player, task: Task):
    try:
        self.players_manager.can_start_game(player)
        self.players_manager.draw_starting_player()
        self.end_phase()
    except (ServerException, ValidationError) as e:
        raise e


# picking characters


def pick_starting_character_2(
    self, player: Player, task: StartingCharacterPick
) -> None:
    self.stop_timer()
    if task.character_name in self.players_manager.image_names["names"]:
        player.set_character(task.character_name)
    self._can_start()


def _pick_random_character(self, player: Player):
    print("CALLED")
    random_character = random.choice(self.players_manager.image_names)
    player.set_character(random_character)
    self.final_message = (
        self.validator(character_name=random_character),
        2,
    )
    self._can_start()


def _can_start(self):
    if self.players_manager.all_playes_characters_picked():
        characters_picked_task = CharactersPicked(task="characters_picked")
        self.final_message = (characters_picked_task, 0)
        self.end_phase()


# asking & answering questions; guessing the character
def ask_question_1(self, player: Player, task: QuestionAsk) -> None:
    if self.players_manager.currently_asking_player == None:
        raise ServerException(errors_by_code["ASKING_PLAYER_NOT_SPECIFIED"])
    if player.game_id != self.players_manager.currently_asking_player:
        raise ServerException(errors_by_code["INVALID_ASKING_PLAYER"])


def answer_question(self, player: Player, task: QuestionAsk) -> None:
    if self.players_manager.currently_asking_player == None:
        raise ServerException(errors_by_code["ASKING_PLAYER_NOT_SPECIFIED"])
    if player.game_id == self.players_manager.currently_asking_player:
        raise ServerException(errors_by_code["INVALID_ASKING_PLAYER"])
    if task.answer != "idk":
        self.players_manager.change_currently_asking_player()


def guess_character(self, player: Player, task: QuestionAsk) -> None:
    if task.character_name not in self.players_manager.image_names:
        assert ServerException("This character doesn't exist!")
    if self.players_manager.get_enemy(player).character == task.character_name:
        self.final_message = (
            GameEnd(character_name=player.character, winner_id=player.game_id),
            0,
        )
        self.end_phase()
