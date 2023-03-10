from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Integer, String, text, ForeignKey, Table
from sqlalchemy.orm import relationship

from sqlalchemy.types import ARRAY
from .database import Base
from .types import Role, Category


users_to_events_table = Table(
    "users_to_events",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("event_id", Integer, ForeignKey("events.id")),
)


users_to_friends_table = Table(
    "users_to_friends",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("friend_id", Integer, ForeignKey("users.id")),
)


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


# upload_image -> backend -> id; id_image ->
# TODO: AWS S3
class EventImage(Base):
    __tablename__ = "event_images"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # optional
    url = Column(String, nullable=False)


class EventSchedule(Base):
    __tablename__ = "event_schedules"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # optional
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)  #
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    description = Column(String, nullable=False)

    # relations
    event_id = Column(Integer, ForeignKey("events.id"))


class EventComment(Base):
    __tablename__ = "event_comments"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # relations
    from_user_id = Column(Integer, ForeignKey("users.id"))
    from_user = relationship("User", back_populates="comments")
    event_id = Column(Integer, ForeignKey("events.id"))


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # require
    categories = Column(ARRAY(Enum(Category)), nullable=False, default=[])
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # optional 
    link_to_registration = Column(String, nullable=True)
    link_to_buy_ticket = Column(String, nullable=True)

    # relations
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="created_events")
    participants = relationship(
        "User", secondary=users_to_events_table, back_populates="participant_events"
    )
    schedules = relationship("EventSchedule")
    comments = relationship("EventComment")