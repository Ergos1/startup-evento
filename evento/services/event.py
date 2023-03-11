from fastapi import HTTPException

from evento.database import session_scope
from evento.models import Event, EventCategory, EventSchedule, User
from evento.types import (
    BasePaginationFilter,
    CreateEventSchema,
    EventOutSchema,
    SubscribeSchema,
)


def create_event(payload: CreateEventSchema, user_id: int):
    with session_scope() as db:
        new_event = Event(
            **payload.dict(exclude={"schedules": True, "category_ids": True}),
            creator_id=user_id,
        )

        categories = (
            db.query(EventCategory)
            .filter(EventCategory.id.in_(payload.category_ids))
            .all()
        )
        new_event.categories += categories

        schedules = list(
            map(
                lambda schedule: EventSchedule(
                    start_date=schedule.start_date,
                    end_date=schedule.end_date,
                    description=schedule.description,
                ),
                payload.schedules,
            )
        )
        db.add_all(schedules)
        new_event.schedules += schedules

        db.add(new_event)
        db.flush()
        db.refresh(new_event)

        return EventOutSchema.from_orm(new_event)


def get_event_list(payload: BasePaginationFilter) -> list[EventOutSchema]:
    with session_scope() as db:
        events = db.query(Event).offset(payload.offset()).limit(payload.limit).all()
        return [EventOutSchema.from_orm(event) for event in events]


def get_event(event_id: int) -> EventOutSchema:
    with session_scope() as db:
        event = db.query(Event).filter(Event.id == event_id).one_or_none()

        if event is None:
            raise HTTPException(400, "Event not found")

        return EventOutSchema.from_orm(event)


def subscribe(payload: SubscribeSchema, user_id: int):
    """Subscribe user to event and return ```numbers of subscribers```"""
    with session_scope() as db:
        event = db.query(Event).filter(Event.id == payload.event_id).one_or_none()

        if event is None:
            raise HTTPException(400, "Event not found")

        user = db.query(User).filter(User.id == user_id).one()

        event.participants.append(user)

        db.add(event)
        db.flush()
        db.refresh(event)

        return (
            db.query(User)
            .join(User.participant_events)
            .filter(Event.id == event.id)
            .count()
        )
