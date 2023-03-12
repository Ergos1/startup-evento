from fastapi import HTTPException

from evento.database import session_scope
from evento.models import Event, EventCategory, EventSchedule, User
from evento.types import (
    CreateEventSchema,
    EventListSchema,
    EventOutSchema,
    SubscribeInSchema,
    SubscribeOutSchema,
)


def create_event(payload: CreateEventSchema, user: User):
    with session_scope() as db:
        new_event = Event(
            **payload.dict(exclude={"schedules": True, "category_ids": True}),
            creator_id=user.id,
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


def get_event_list(payload: EventListSchema, user: User) -> list[EventOutSchema]:
    with session_scope() as db:
        events_qb = db.query(Event)

        if user is not None:
            if payload.only_subscribed:
                events_qb = events_qb.join(Event.participants).filter(
                    User.id == user.id
                )

        events = events_qb.offset(payload.offset()).limit(payload.limit).all()

        return [EventOutSchema.from_orm(event) for event in events]


def get_event(event_id: int, user: User | None) -> EventOutSchema:
    with session_scope() as db:
        event = db.query(Event).filter(Event.id == event_id).one_or_none()

        if event is None:
            raise HTTPException(400, "Event not found")

        event_out = EventOutSchema.from_orm(event)

        if user is not None:
            event_out.is_subscribed = user.id in [
                user.id for user in event.participants
            ]

        return event_out


def subscribe(payload: SubscribeInSchema, user: User) -> SubscribeOutSchema:
    """Subscribe user to event and return ```numbers of subscribers```"""
    with session_scope() as db:
        event = db.query(Event).filter(Event.id == payload.event_id).one_or_none()

        if event is None:
            raise HTTPException(400, "Event not found")

        user = db.query(User).filter(User.id == user.id).one()

        event.participants.append(user)

        db.add(event)
        db.flush()
        db.refresh(event)

        return SubscribeOutSchema(
            participantsCount=db.query(User)
            .join(User.participant_events)
            .filter(Event.id == event.id)
            .count()
        )
