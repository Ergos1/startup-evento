from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from evento.services import login_user, register_user, send_otp, verify_otp
from evento.types import (
    LoginUserSchema,
    RegisterUserSchema,
    SendOTPSchema,
    VerifyOTPSchema,
)

router = APIRouter()


@router.post("/register")
def register(payload: RegisterUserSchema):
    return register_user(payload=payload)


@router.post("/login")
def login(payload: LoginUserSchema):
    return login_user(payload=payload)


@router.post("/send-otp")
def send_otp_(payload: SendOTPSchema):
    return send_otp(payload)


@router.post("/verify-otp")
def verify_otp_(payload: VerifyOTPSchema):
    return verify_otp(payload)
