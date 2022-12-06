class ServerException(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message: str = message


class CriticalServerException(Exception):
    pass


errors_by_code = {
    "ASKING_PLAYER_NOT_SPECIFIED": "Server error.",
    "INVALID_ASKING_PLAYER": "It's enemy's turn to ask.",
    "NONEXISTENT CHARACTER": "Picked character doesn't exist. Could'd be a server error.",
}
