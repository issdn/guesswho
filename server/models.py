from typing import Optional, Union, Literal
from pydantic import BaseModel

TaskType = Literal["player_ready", "player_leave", "player_join", "set_creator"]


class Action(BaseModel):
    type: Literal["task", "init", "error", "info"]
    data: object


class Init(BaseModel):
    nickname: str


class Task(BaseModel):
    task: TaskType


class Error(BaseModel):
    message: str


class Info(BaseModel):
    task: Optional[TaskType]
    nickname: str
    creator: bool
    lobby_id: int


action_types = {"task": Task, "init": Init, "error": Error, "info": Info}
