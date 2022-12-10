from typing import Optional, Literal
from pydantic import BaseModel

class BaseTaskModel(BaseModel):
    task: Literal["player_ready","start_game"]
    game_id: Optional[int]


class PlayerLeaveModel(BaseModel):
    task: Literal["player_leave"]
    game_id: int
    new_creator_game_id: int


class PlayerJoinModel(BaseModel):
    task: Literal["player_join"]
    nickname: str


class PlayerInitInfoModel(BaseModel):
    creator: bool
    ready: bool
    nickname: str
    game_id: int


class PlayerJoinResponseModel(BaseModel):
    task: Literal["player_join"]
    game_id: int
    players: list[PlayerInitInfoModel]


class ErrorModel(BaseModel):
    type: Literal["error"] = "error"
    message: str
    field: Optional[str] = None


class StartingCharacterPickModel(BaseTaskModel):
    task: Literal["pick_starting_character"] = "pick_starting_character"
    character_name: str
    overtime: bool = False


class HelperMessageModel(BaseModel):
    task: Literal[
        "characters_picked", "asking_overtime", "answering_overtime", "guess_character"
    ]
    game_id: Optional[int]


class QuestionModel(BaseTaskModel):
    task: Literal["ask_question", "answer_question", "guess_character"]
    question: Optional[str]
    answer: Optional[Literal["yes", "no", "idk"]]
    character_name: Optional[str]


class GameEndModel(BaseModel):
    task: Literal["game_end", "restart_game"] = "game_end"
    winner_id: Optional[int]
    game_id: Optional[int]
    character_name: Optional[str]
