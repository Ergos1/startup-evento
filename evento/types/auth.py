from pydantic import BaseModel, Field

from .constraints import Password, PhoneNumber, Username
from .user import Role


class RegisterUserSchema(BaseModel):
    """DTO for register user"""

    username: Username  # unique
    phone_number: PhoneNumber = Field(alias="phoneNumber")
    password: Password
    role: Role

    class Config:
        allow_population_by_field_name = True


class LoginUserSchema(BaseModel):
    """DTO for login user"""

    phone_number: PhoneNumber = Field(alias="phoneNumber")
    password: Password

    class Config:
        allow_population_by_field_name = True


class TokenSchema(BaseModel):
    """DTO for auth token"""

    token: str


class SendOTPSchema(BaseModel):
    """DTO for send otp"""

    phone_number: PhoneNumber = Field(alias="phoneNumber")

    class Config:
        allow_population_by_field_name = True


class VerifyOTPSchema(BaseModel):
    """DTO for send otp"""

    otp_code: str = Field(alias="otpCode")
    phone_number: PhoneNumber = Field(alias="phoneNumber")

    class Config:
        allow_population_by_field_name = True
