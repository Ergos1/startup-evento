from fastapi import APIRouter

from evento.services import login_user, register_user, send_otp, verify_otp
from evento.types import (
    LoginUserSchema,
    RegisterUserSchema,
    SendOTPSchema,
    TokenSchema,
    UserOutSchema,
    VerifyOTPSchema,
)

router = APIRouter()


@router.post("/register", response_model=UserOutSchema)
def register(payload: RegisterUserSchema):
    return register_user(payload=payload)


@router.post("/login", response_model=TokenSchema)
def login(payload: LoginUserSchema):
    return login_user(payload=payload)


@router.post("/send-otp")
def send_otp_(payload: SendOTPSchema):
    return send_otp(payload)


@router.post("/verify-otp")
def verify_otp_(payload: VerifyOTPSchema):
    return verify_otp(payload)
