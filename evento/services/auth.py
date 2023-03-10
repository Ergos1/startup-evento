from datetime import datetime, timedelta
from typing import cast

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from requests import get
from sqlalchemy import or_
from sqlalchemy.orm import Session

from evento.database import session_scope
from evento.execeptions import UserNotFoundException
from evento.models import User
from evento.settings import settings
from evento.tools import generate_otp, hash_password, verify_password
from evento.types import (
    LoginUserSchema,
    RegisterUserSchema,
    SendOTPSchema,
    TokenSchema,
    UserOutSchema,
    VerifyOTPSchema,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependecy to get user from auth token"""

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("sub", None) is None:
            raise Exception
    except Exception as e:
        print(e)
        raise HTTPException(401, "Unauthorized")

    with session_scope() as db:
        user = db.query(User).filter(User.id == 1).one_or_none()
        if user is None:
            raise UserNotFoundException()

        return user


def register_user(payload: RegisterUserSchema) -> UserOutSchema:
    with session_scope() as db:
        user = (
            db.query(User)
            .filter(
                or_(
                    User.phone_number == payload.phone_number,
                    User.username == payload.username,
                )
            )
            .one_or_none()
        )
        if user is not None:
            raise HTTPException(422, "User phone number or username is not unique")

        new_user = User(**payload, hash_password=hash_password(payload.password))
        db.add(new_user)
        db.commit()

        return UserOutSchema.from_orm(new_user)


def login_user(payload: LoginUserSchema) -> TokenSchema:
    with session_scope() as db:
        user = (
            db.query(User)
            .filter(User.phone_number == payload.phone_number)
            .one_or_none()
        )

        if not user:
            raise UserNotFoundException()

        if not user.verified:
            raise HTTPException(400, "User is not verified")

        if not verify_password(payload.password, cast(str, user.hash_password)):
            raise HTTPException(400, "Incorrect password")

        expire = datetime.utcnow() + timedelta(minutes=1000000)
        access_token = jwt.encode(
            {"sub": user.id, "exp": expire},
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        return TokenSchema(token=access_token)


def send_otp(payload: SendOTPSchema) -> None:
    """Sends OTP to phone number otherwise raise ```Exception```"""

    with session_scope() as db:
        user = (
            db.query(User)
            .filter(User.phone_number == payload.phone_number)
            .one_or_none()
        )

        if not user:
            raise UserNotFoundException()

        if user.verified:
            raise HTTPException(400, "User already verified")

        otp_code = generate_otp(6)

        phone_number = cast(str, user.phone_number).replace("+", "")
        response = get(
            settings.OTP_API_URL,
            params={
                "recipient": phone_number,
                "text": f"Код верификации: {otp_code} \nНИКОМУ НЕ ГОВОРИТЕ КОД!",
                "apiKey": settings.OTP_API_KEY,
            },
        )

        if response.json().get("code", 1) != 0:
            raise HTTPException(500, "OTP provider is unaviable")

        return None


def verify_otp(payload: VerifyOTPSchema) -> None:
    """Verifies OTP otherwise raise ```Exception```"""

    with session_scope() as db:
        user = (
            db.query(User)
            .filter(User.phone_number == payload.phone_number)
            .one_or_none()
        )

        if not user:
            raise UserNotFoundException()

        if user.verified:
            raise HTTPException(400, "User already verified")

        if user.otp_code != payload.otp_code:
            raise HTTPException(400, "OTP is incorrect")

        user.verified = True  # type: ignore
        db.commit()

        return None
