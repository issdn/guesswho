import functools
from typing import Literal
from pydantic import ValidationError
from players_manager import Player
from models import (
    HelperMessages,
    GameEnd,
    PlayerJoin,
    QuestionAsk,
    StartingCharacterPick,
    Task,
)
from errors import ServerException, errors_by_code
from config import Config


def clear_function_name(function_name: str) -> tuple[str, int]:
    task_name_split = function_name.split("_")
    if task_name_split[-1].isnumeric():
        clear_name = "_".join(task_name_split[:-1])
        broadcast_function_number = int(task_name_split[-1])
    else:
        clear_name = function_name
        broadcast_function_number = 0
    return (clear_name, broadcast_function_number)


class BasePhase:
    """
    Phases are main pieces of logic here.
    A whole life cycle is chronologically divided into phases
    and every phase is divided into asynchronous tasks.
    Every phase has it's own validator(model) for tasks.

    So, during PlayersJoinPhase the client can only send player_join task,
    which structure is defined by PlayerJoin validator.

    To end a phase, use end_phase() method.

    Therefore special naming is needed for every function:
        - standard underscore-separated naming, like: pick_starting_character and
        - adequate number-key of a broadcast function, like: 2 (broadcasting only to the player sending the message).
        Thus the dictionary self.tasks will contain: { 'pick_starting_character_2' <string> : (pick_starting_character <function>, 2 <int>) }.
    """

    def __init__(self, players_manager, message_queue, shift_phases):
        self.tasks: dict[str, tuple[callable, int]] = self._get_tasks()
        self._players_manager = players_manager
        self._message_queue = message_queue
        self._shift_phases = shift_phases

    def _get_tasks(self) -> dict[str, tuple[callable, int]]:
        """
        This function takes all the public methods
        """
        tasks = {}
        for key in self.__class__.__dict__.keys():
            if not key.startswith("_"):
                clear_name, broadcast_function_number = clear_function_name(key)
                tasks[clear_name] = (getattr(self, key), broadcast_function_number)
        return tasks


class PlayersJoinPhase(BasePhase):
    def __init__(self, players_manager, message_queue, shift_phases):
        super().__init__(players_manager, message_queue, shift_phases)
        self.validator = PlayerJoin

    async def player_join_3(self, player: Player, task: PlayerJoin) -> None:
        """
        Set player's nickname taken from the task, add player to players_manager<PlayersManager>.
        If the lobby is full (2 players), end the phase.
        """
        player.set_nickname(task.nickname)
        self._players_manager.add_player(player)
        self._message_queue.timed_tasks_allocate_player_key(player.game_id)
        if len(self._players_manager.players) == 2:
            self._shift_phases()


class LobbyPhase(BasePhase):
    def __init__(self, players_manager, message_queue, shift_phases):
        super().__init__(players_manager, message_queue, shift_phases)
        self.validator = Task

    async def player_ready(self, player: Player, task: Task) -> None:
        player.switch_ready()

    async def start_game(self, player: Player, task: Task):
        try:
            self._players_manager.can_start_game(player)
            self._players_manager.draw_starting_player()
            self._shift_phases()
        except (ServerException, ValidationError) as e:
            raise e


class GamePrepPhase(BasePhase):
    def __init__(self, players_manager, message_queue, shift_phases):
        super().__init__(players_manager, message_queue, shift_phases)
        self.validator = StartingCharacterPick
        for game_player in self._players_manager.players:
            self._message_queue.add_timed_task(
                player_game_id=game_player.game_id,
                time=Config.PICKING_CHARACTER_TIME,
                ending_task_name="pick_starting_character",
                overtime_callback=self._pick_random_character,
                additional_params=(game_player,),
            )

    async def pick_starting_character_2(
        self, player: Player, task: StartingCharacterPick
    ) -> None:
        if task.character_name in self._players_manager.image_names:
            player.set_character(task.character_name)
        await self._can_start()

    async def _pick_random_character(self, player: Player):
        random_character = self._players_manager.draw_random_character_name()
        player.set_character(random_character)
        await self._message_queue.send_message(
            2, self.validator(character_name=random_character), player
        )
        await self._can_start()

    async def _can_start(self):
        if self._players_manager.all_playes_characters_picked():
            await self._message_queue.send_message(
                0,
                HelperMessages(
                    task="characters_picked",
                    game_id=self._players_manager.currently_asking_player_game_id,
                ),
            )
            self._shift_phases()


class GamePhase(BasePhase):
    def __init__(self, players_manager, message_queue, shift_phases):
        super().__init__(players_manager, message_queue, shift_phases)
        self.validator = QuestionAsk
        self._message_queue.add_timed_task(
            self._players_manager.currently_asking_player_game_id,
            Config.ASKING_TIME,
            "ask_question",
            self._ask_answer_overtime,
            ("asking_overtime",),
        )

    async def ask_question_1(self, player: Player, task: QuestionAsk) -> None:
        self._check_asking_player_specified()
        self._check_correct_player_asking(player)
        if player.game_id != self._players_manager.currently_asking_player_game_id:
            raise ServerException(errors_by_code["INVALID_ASKING_PLAYER"])
        self._message_queue.add_timed_task(
            self._players_manager.currently_answering_player_game_id,
            Config.ASKING_TIME,
            "answer_question",
            self._ask_answer_overtime,
            ("answering_overtime", "answer_question"),
        )

    async def answer_question(self, player: Player, task: QuestionAsk) -> None:
        self._check_asking_player_specified()
        self._check_correct_player_answering(player)
        if task.answer != "idk":
            self._players_manager.change_currently_asking_player_game_id()

    async def guess_character(self, player: Player, task: QuestionAsk) -> None:
        if task.character_name not in self._players_manager.image_names:
            assert ServerException("This character doesn't exist!")
        if self._players_manager.get_enemy(player).character == task.character_name:
            await self._message_queue.send_message(
                0, GameEnd(character_name=player.character, winner_id=player.game_id)
            )
            self._shift_phases()

    async def _ask_answer_overtime(
        self, task_name: str, next_task: Literal["ask_question", "answer_question"]
    ) -> None:
        self._players_manager.change_currently_asking_player_game_id()
        await self._message_queue.send_message(0, HelperMessages(task=task_name))
        _next_task = (
            "ask_question" if next_task == "answer_question" else "answer_question"
        )
        self._message_queue.add_timed_task(
            self._players_manager.currently_answering_player_game_id,
            Config.ASKING_TIME,
            "answer_question",
            self._ask_answer_overtime,
            ("answering_overtime", _next_task),
        )

    def _check_asking_player_specified(self) -> None:
        if self._players_manager.currently_asking_player_game_id == None:
            raise ServerException(errors_by_code["ASKING_PLAYER_NOT_SPECIFIED"])

    def _check_correct_player_asking(self, player: Player) -> None:
        if player.game_id != self._players_manager.currently_asking_player_game_id:
            raise ServerException(errors_by_code["INVALID_ASKING_PLAYER"])

    def _check_correct_player_answering(self, player: Player) -> None:
        if player.game_id == self._players_manager.currently_asking_player_game_id:
            raise ServerException(errors_by_code["INVALID_ASKING_PLAYER"])
