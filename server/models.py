from typing import Optional, Literal, Union
from pydantic import BaseModel

TaskType = Union[
    Literal["player_leave"],
    Literal["player_join"],
    Literal["player_ready"],
    Literal["pick_starting_character"],
    Literal["start_game"],
]


class Task(BaseModel):
    task: TaskType
    game_id: Optional[int]


class PlayerJoin(BaseModel):
    task: Literal["player_join"]
    nickname: str


class PlayerInitInfo(BaseModel):
    creator: bool
    ready: bool
    nickname: str
    game_id: int


class PlayerJoinResponse(Task):
    players: list[PlayerInitInfo]


class Error(BaseModel):
    type: Literal["error"] = "error"
    message: str
    field: Optional[str] = None


class StartingCharacterPick(Task):
    character_name: str


class QuestionAsk(Task):
    question: str
    answer: Optional[str]
