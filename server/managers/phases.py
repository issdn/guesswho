from pydantic import ValidationError
from managers.player import Player
from models import (
    PlayerJoin,
    QuestionAsk,
    StartingCharacterPick,
    Task,
)
from errors import ServerException


class BasePhase:
    """
    Description

    This class manages tasks (functions) that process messages from the socket.
    To divide tasks into separate phases - inherit this class.
    Eg.: tasks from phase<Lobby(BasePhase)> will take players_manager<PlayerManager> and player<Player> object as parameters
        and phase<Game(BasePhase)> will additionally take task<Task> as parameters.
        Thus the actual calling of the tasks (functions) will require less logic because the functions are already subdivided.

    (?) Class for tasks (functions) that process messages sent by the user through the websocket.
        The class gathers all functions and puts them in a dictionary with task name as string key
        and tuple of function pointer (callable) and integer key for broadcast function that the task will be sent over through.
        Functions can return only an error instanciated from an Error or a ValidationError class.

    The idea behind this design is taken from Spring Boot Persistence JPA where tables, cols etc. are automatically created from a POJO,
    from attributes with special decorators. No decorators in this case because it seems to be too small for such complex system..

    (!) Therefore special naming is needed for every function:
        - standard underscore-separated naming, like: pick_starting_character and
        - adequate number-key of a broadcast function, like: 2 (broadcasting only to the player sending the message).
        Thus the dictionary self.tasks will contain: { 'pick_starting_character_2' <string> : (pick_starting_character <function>, 2 <int>) }.

    TL;DR (not full though) - method name eg.: pick_starting_character_2, where pick_starting_character is the name and _2 is the number of a broadcast function.
    """

    def __init__(self, players_manager):
        self.tasks: dict[callable, int] = self._get_tasks()
        self.name = self.__class__.__name__.lower()
        self.running = False
        self.players_manager = players_manager

    def _get_tasks(self) -> dict[callable, int]:
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


class PlayersJoinPhase(BasePhase):
    def __init__(self, players_manager):
        super().__init__(players_manager)
        self.validator = PlayerJoin

    def player_join_3(self, player: Player, task: PlayerJoin) -> None:
        player.set_nickname(task.nickname)
        self.players_manager.add_player(player)
        self.running = False
        print(self.running)


class LobbyPhase(BasePhase):
    def __init__(self, players_manager):
        super().__init__(players_manager)
        self.validator = Task

    def player_ready(self, player: Player, task: Task) -> None:
        player.switch_ready()

    def player_leave(self, player: Player, task: Task) -> None:
        self.players_manager.player_leave(player)

    def start_game(self, player: Player, task: Task):
        try:
            self.players_manager.can_start_game(player)
        except (ServerException, ValidationError) as e:
            raise e


class GamePrepPhase(BasePhase):
    def __init__(self, players_manager):
        super().__init__(players_manager)
        self.validator = StartingCharacterPick

    def pick_starting_character_2(
        self, player: Player, task: StartingCharacterPick
    ) -> None:
        if task.character_name in self.players_manager.image_names:
            player.character = task.character_name

    def player_leave(self, player: Player, task: Task) -> None:
        self.players_manager.player_leave(player)


class GamePhase(BasePhase):
    def __init__(self, players_manager):
        super().__init__(players_manager)
        self.validator = QuestionAsk

    def send_question_1(player: Player, task: QuestionAsk) -> None:
        pass

    def answer_question_1(player: Player, task: QuestionAsk) -> None:
        pass

    def player_leave(self, player: Player, task: Task) -> None:
        self.players_manager.player_leave(player)
