from typing import Optional, Literal, Union
from pydantic import BaseModel

TaskType = Union[
    Literal["player_leave"],
    Literal["player_join"],
    Literal["player_ready"],
    Literal["start"],
]


class Task(BaseModel):
    task: TaskType
    lobby_id: Optional[int]


class PlayerJoin(BaseModel):
    task: Literal["player_join"]
    nickname: str


class PlayerInitInfo(BaseModel):
    creator: bool
    ready: bool
    nickname: str
    lobby_id: int


class PlayerJoinResponse(Task):
    players: list[PlayerInitInfo]


class Error(BaseModel):
    type: Literal["error"] = "error"
    message: str
    field: Optional[str] = None
