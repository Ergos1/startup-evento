import re
from enum import Enum

from pydantic import BaseModel, validator

from evento.tools import hash_password


class PhoneNumber(str):
    """Validate phone number"""

    regex = r"^\+\d{11}$"

    @validator("value")
    def validate_phone(cls, value):
        if not re.match(cls.regex, value):
            raise ValueError("Invalid phone number format")
        return value


class Password(str):
    """Validate password"""

    @validator("value")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password length must be more or equal 8")

        return value


class Role(str, Enum):
    """User roles"""

    USER = "USER"
    ORGANIZER = "ORGANIZER"


class Username(str):
    regex = r"[A-Za-z]{1}[A-Za-z0-9]{4,32}"

    @validator("value")
    def validate_username(cls, value):
        if not re.match(cls.regex, value):
            raise ValueError("Invalid username format")
        return value


class UserOutSchema(BaseModel):
    """DTO for user response"""

    username: Username
    phone_number: PhoneNumber
    role: Role

    @staticmethod
    def from_orm(user):
        return UserOutSchema(**user)
