from enum import Enum

from pydantic import BaseModel, Field

from .constraints import Password, PhoneNumber, Username


class Role(str, Enum):
    """User roles"""

    USER = "USER"
    ORGANIZER = "ORGANIZER"


class AddFriendSchema(BaseModel):
    """DTO for add friend"""

    friend_phone_number: PhoneNumber = Field(alias="friendPhoneNumber")

    class Config:
        allow_population_by_field_name = True


class UserOutSchema(BaseModel):
    """DTO for user response"""

    username: Username
    phone_number: PhoneNumber = Field(alias="phoneNumber")
    role: Role

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
