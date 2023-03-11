from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY

from .database import Base
from .types import Role

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


events_to_events_categories_table = Table(
    "events_to_event_categories",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("event_category_id", Integer, ForeignKey("event_categories.id")),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # require
    password = Column(String, nullable=False)
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

    # relations
    participant_events = relationship(
        "Event",
        secondary=users_to_events_table,
        back_populates="participants",
    )

    friends = relationship(
        "User",
        secondary=users_to_friends_table,
        primaryjoin=id == users_to_friends_table.c.user_id,
        secondaryjoin=id == users_to_friends_table.c.friend_id,
        backref="friends_backref",
    )
    created_events = relationship("Event", back_populates="creator")
    comments = relationship("EventComment", back_populates="from_user")


# upload_image -> backend -> id; id_image ->
# TODO: AWS S3
class EventImage(Base):
    __tablename__ = "event_images"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # require
    url = Column(String, nullable=False)

    # relations
    event_id = Column(Integer, ForeignKey("events.id"))


class EventSchedule(Base):
    __tablename__ = "event_schedules"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # optional
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
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


class EventCategory(Base):
    __tablename__ = "event_categories"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # require
    name = Column(String, nullable=False)

    # relations
    events = relationship(
        "Event",
        secondary=events_to_events_categories_table,
        back_populates="categories",
    )


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    # require
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # optional
    link_to_registration = Column(String, nullable=True)
    link_to_buy_ticket = Column(String, nullable=True)

    # relations
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="created_events", lazy="joined")
    participants = relationship(
        "User",
        secondary=users_to_events_table,
        back_populates="participant_events",
        lazy="select",
    )
    schedules = relationship("EventSchedule", lazy="select")
    comments = relationship("EventComment", lazy="select")
    images = relationship("EventImage", lazy="select")
    categories = relationship(
        "EventCategory",
        secondary=events_to_events_categories_table,
        back_populates="events",
        lazy="select",
    )
