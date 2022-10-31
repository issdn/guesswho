from typing import Optional, Literal
from pydantic import BaseModel

TaskType = Literal["player_ready", "player_leave", "player_join", "set_creator", "init"]


class InfoBase(BaseModel):
    nickname: Optional[str]
    creator: Optional[bool]
    lobby_id: Optional[int]
    ready: Optional[bool]


class Task(InfoBase):
    type: Literal["task"]
    task: TaskType


class Error(BaseModel):
    type: Literal["error"]
    message: str
    field: Optional[str] = None


class Info(InfoBase):
    type: Literal["info"]
    task: Optional[TaskType]


action_types = {"task": Task, "error": Error, "info": Info}
