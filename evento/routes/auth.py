from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from evento.database import get_db
from evento.services import login_user, register_user, send_otp, verify_otp
from evento.types import (
    LoginUserSchema,
    RegisterUserSchema,
    SendOTPSchema,
    VerifyOTPSchema,
)

router = APIRouter()


@router.post("/register")
def register(payload: RegisterUserSchema, db: Session = Depends(get_db)):
    return register_user(payload=payload, db=db)


@router.post("/login")
def login(payload: LoginUserSchema, db: Session = Depends(get_db)):
    return login_user(payload=payload, db=db)


@router.post("/send-otp")
def send_otp_(payload: SendOTPSchema, db: Session = Depends(get_db)):
    return send_otp(payload, db)


@router.post("/verify-otp")
def verify_otp_(payload: VerifyOTPSchema, db: Session = Depends(get_db)):
    return verify_otp(payload, db)
