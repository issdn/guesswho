from fastapi import WebSocket
from pydantic import ValidationError

from models import Error


class ServerException(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message: str = message


class CriticalServerException(Exception):
    pass
