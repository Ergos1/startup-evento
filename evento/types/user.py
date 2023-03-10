import re
from enum import Enum

from pydantic import BaseModel

from .constraints import Password, PhoneNumber, Username


class Role(str, Enum):
    """User roles"""

    USER = "USER"
    ORGANIZER = "ORGANIZER"


class AddFriendSchema(BaseModel):
    """DTO for add friend"""

    friend_phone_number: PhoneNumber


class UserOutSchema(BaseModel):
    """DTO for user response"""

    username: Username
    phone_number: PhoneNumber
    role: Role

    class Config:
        orm_mode = True
