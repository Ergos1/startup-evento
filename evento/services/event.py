from fastapi import HTTPException

from evento.database import session_scope
from evento.models import (
    Event,
    EventSchedule,
    events_to_events_categories_table,
    users_to_events_table,
)
from evento.types import (
    BasePaginationFilter, 
    CreateEventSchema, 
    GetEventOutSchema, 
    SubscribeSchema,
)


def create_event(payload: CreateEventSchema, user_id: int):
    with session_scope() as db:
        new_event = Event(
            **payload.dict(exclude={"schedules": True, "category_ids": True}),
            creator_id=user_id,
        )

        # TODO: make it more reliable
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        for category in payload.categories:
            new_event_to_category = events_to_events_categories_table.insert().values(
                event_id=new_event.id,
                event_category_id=category.id,
            )
            db.execute(new_event_to_category)

        for schedule in payload.schedules:
            new_schedule = EventSchedule(
                start_date=schedule.start_date,
                end_date=schedule.end_date,
                event_id=new_event.id,
                description=schedule.description,
            )
            db.add(new_schedule)

        return


def get_event_list(payload: BasePaginationFilter) -> list[GetEventOutSchema]:
    with session_scope() as db:
        events = db.query(Event).offset(payload.offset()).limit(payload.size).all()
        return list(map(lambda event: GetEventOutSchema.from_orm(event), events))


def get_event(event_id: int) -> GetEventOutSchema:
    with session_scope() as db:
        event = db.query(Event).filter(Event.id == event_id).one_or_none()

        if event is None:
            raise HTTPException(400, "Event not found")

        return GetEventOutSchema.from_orm(event)


def subscribe(payload: SubscribeSchema, user_id: int):
    with session_scope() as db:
        event = db.query(Event).filter(Event.id == payload.event_id).one_or_none()

        if event is None:
            raise HTTPException(400, "Event not found")
    
        new_user_to_event = users_to_events_table.insert().values(
            user_id=user_id,
            event_id=payload.event_id,
        )
        db.execute(new_user_to_event)

        return
