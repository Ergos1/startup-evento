from random import choices
from string import ascii_uppercase, digits

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def generate_otp(length: int) -> str:
    return "".join(choices(ascii_uppercase + digits, k=length))
