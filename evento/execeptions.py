from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    """Status code = ```400``` and detail = ```User not found```"""

    def __init__(self) -> None:
        super().__init__(400, "User not found", None)
