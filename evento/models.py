from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Integer, String, text

from .database import Base
from .types import Role


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # require
    hash_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    phone_number = Column(String, nullable=False, unique=True, index=True)

    # optional
    surname = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    otp_code = Column(String, nullable=True)
    verified = Column(Boolean, nullable=True, server_default="False")

    # extension
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
