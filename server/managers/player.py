from fastapi import WebSocket
from starlette.datastructures import Address

from models import PlayerInitInfo, Task, TaskType


class Player:
    def __init__(self, nickname: str, websocket: WebSocket):
        self.nickname: str = nickname
        self.websocket: WebSocket = websocket
        self.address: Address = websocket.client
        self.lobby_id: int = None
        self.creator: bool = False
        self.ready: bool = False

    def switch_ready(self):
        self.ready = not self.ready

    def switch_creator(self):
        self.creator = not self.creator

    def set_nickname(self, nickname: str):
        self.nickname = nickname

    def get_init_info(self):
        return PlayerInitInfo(
            nickname=self.nickname,
            creator=self.creator,
            ready=self.ready,
            lobby_id=self.lobby_id,
        )

    def get_task(self, task_type: TaskType) -> Task:
        return Task(task=task_type, lobby_id=self.lobby_id).json()
