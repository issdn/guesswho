from typing import Optional, Literal
from pydantic import BaseModel

TaskTypes = Literal[
    "player_leave",
    "player_ready",
    "pick_starting_character",
    "start_game",
    "characters_picked",
]


class Task(BaseModel):
    task: TaskTypes
    game_id: Optional[int]


class PlayerJoin(BaseModel):
    task: Literal["player_join"]
    nickname: str


class PlayerInitInfo(BaseModel):
    creator: bool
    ready: bool
    nickname: str
    game_id: int


class PlayerJoinResponse(BaseModel):
    task: Literal["player_join"]
    game_id: int
    players: list[PlayerInitInfo]


class Error(BaseModel):
    type: Literal["error"] = "error"
    message: str
    field: Optional[str] = None


class StartingCharacterPick(Task):
    character_name: str


class QuestionAsk(Task):
    task: Literal["ask_question", "answer_question", "guess_character"]
    question: Optional[str]
    answer: Optional[Literal["yes", "no", "idk"]]
    character_name: Optional[str]


class GameEnd(BaseModel):
    task: Literal["game_end"] = "game_end"
    winner_id: Optional[int]
    character_name: Optional[str]
    restart: Optional[bool]
