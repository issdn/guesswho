from typing import Optional, Literal
from pydantic import BaseModel

TaskType = Literal["player_ready", "player_leave", "player_join", "set_creator"]


class Init(BaseModel):
    type: Literal["init"]
    nickname: str


class Task(BaseModel):
    type: Literal["task"]
    task: TaskType


class Error(BaseModel):
    type: Literal["error"]
    message: str
    field: Optional[str] = None


class Info(BaseModel):
    type: Literal["info"]
    task: TaskType
    nickname: Optional[str]
    creator: Optional[bool]
    lobby_id: Optional[int]


action_types = {"task": Task, "init": Init, "error": Error, "info": Info}
