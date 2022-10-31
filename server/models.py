from typing import Optional, Literal, Union
from pydantic import BaseModel, Field

TaskType = Union[
    Literal["player_leave"],
    Literal["player_join"],
    Literal["set_creator"],
    Literal["player_ready"],
]


class Task(BaseModel):
    task: TaskType
    lobby_id: int


class PlayerJoin(BaseModel):
    task: Literal["player_join"]
    nickname: str


class PlayerInitInfo(BaseModel):
    creator: bool
    ready: bool
    nickname: str


class PlayerJoinResponse(Task):
    lobby_id: int
    data: PlayerInitInfo


class Error(BaseModel):
    type: Literal["error"] = "error"
    message: str
    field: Optional[str] = None
