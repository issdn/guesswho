from pydantic import ValidationError
from managers.player import Player
from models import (
    PlayerJoin,
    QuestionAsk,
    StartingCharacterPick,
    Task,
)
from errors import ServerException, errors_by_code


class BasePhase:
    """
    Description

    This class manages tasks (method) that process messages from the socket.
    To divide tasks into separate phases - inherit this class.

    To define a task you need to create a

    Therefore special naming is needed for every function:
        - standard underscore-separated naming, like: pick_starting_character and
        - adequate number-key of a broadcast function, like: 2 (broadcasting only to the player sending the message).
        Thus the dictionary self.tasks will contain: { 'pick_starting_character_2' <string> : (pick_starting_character <function>, 2 <int>) }.
    """

    def __init__(self, players_manager, end_phase: callable, back_to_lobby: callable):
        self.tasks: dict[str, tuple[callable, int]] = self._get_tasks()
        self.name = self.__class__.__name__.lower()
        self.server_message = None
        self.players_manager = players_manager
        self.end_phase = end_phase
        self.back_to_lobby = back_to_lobby

    def _get_tasks(self) -> dict[str, tuple[callable, int]]:
        """
        This function takes all the public methods
        """
        tasks = {}
        for t in dir(self):
            if not t.startswith("_"):
                task_name_split = t.split("_")
                if task_name_split[-1].isnumeric():
                    clear_name = "_".join(task_name_split[:-1])
                    broadcast_function_number = int(task_name_split[-1])
                else:
                    clear_name = t
                    broadcast_function_number = 0
                tasks[clear_name] = (getattr(self, t), broadcast_function_number)
        return tasks

    def player_leave(self, player: Player, task: Task) -> None:
        self.players_manager.player_leave(player)
        self.back_to_lobby()


class PlayersJoinPhase(BasePhase):
    def __init__(self, players_manager, end_phase, back_to_lobby):
        super().__init__(players_manager, end_phase, back_to_lobby)
        self.validator = PlayerJoin

    def player_join_3(self, player: Player, task: PlayerJoin) -> None:
        player.set_nickname(task.nickname)
        self.players_manager.add_player(player)
        if len(self.players_manager.players) == 2:
            self.end_phase()


class LobbyPhase(BasePhase):
    def __init__(self, players_manager, end_phase, back_to_lobby):
        super().__init__(players_manager, end_phase, back_to_lobby)
        self.validator = Task

    def player_ready(self, player: Player, task: Task) -> None:
        player.switch_ready()

    def start_game(self, player: Player, task: Task):
        try:
            self.players_manager.can_start_game(player)
            self.players_manager.draw_starting_player()
            self.end_phase()
        except (ServerException, ValidationError) as e:
            raise e


class GamePrepPhase(BasePhase):
    def __init__(self, players_manager, end_phase, back_to_lobby):
        super().__init__(players_manager, end_phase, back_to_lobby)
        self.validator = StartingCharacterPick

    def pick_starting_character_2(
        self, player: Player, task: StartingCharacterPick
    ) -> None:
        if task.character_name in self.players_manager.image_names["names"]:
            player.set_character(task.character_name)
        if self.players_manager.all_playes_characters_picked():
            characters_picked_task = Task(
                task="characters_picked", game_id=player.game_id
            )
            self.server_message = (characters_picked_task, 0)
            self.end_phase()


class GamePhase(BasePhase):
    def __init__(self, players_manager, end_phase, back_to_lobby):
        super().__init__(players_manager, end_phase, back_to_lobby)
        self.validator = QuestionAsk

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
