class ServerException(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message: str = message


class CriticalServerException(Exception):
    pass


errors_by_code = {
    "ASKING_PLAYER_NOT_SPECIFIED": "Server error.",
    "INVALID_ASKING_PLAYER": "It's enemy's turn to ask.",
}


def get_error(key: str):
    try:
        return ServerException(errors_by_code[key])
    except KeyError:
        print(f"WARNING: Wrong error key.: {key}")
