from pydantic import BaseModel

from .user import Password, PhoneNumber, Role, Username


class RegisterUserSchema(BaseModel):
    """DTO for register user"""

    username: Username  # unique
    phone_number: PhoneNumber  # unique
    password: Password
    role: Role


class LoginUserSchema(BaseModel):
    """DTO for login user"""

    phone_number: PhoneNumber
    password: Password


class TokenSchema(BaseModel):
    """DTO for auth token"""

    token: str


class SendOTPSchema(BaseModel):
    """DTO for send otp"""

    phone_number: PhoneNumber


class VerifyOTPSchema(BaseModel):
    """DTO for send otp"""

    otp_code: str
    phone_number: PhoneNumber
