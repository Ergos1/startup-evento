
from evento.types import CreateEventSchema, BasePaginationFilter, GetEventOutSchema
from evento.database import session_scope
from evento.models import Event, EventSchedule, EventCategory, events_to_events_categories_table

def create_event(payload: CreateEventSchema, user_id: int):
    with session_scope() as db:
        new_event = Event(
            **payload.dict(exclude={"schedules": True, "category_ids": True}),
            creator_id=user_id,
        )
        
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        for category in payload.categories:
            event_category = events_to_events_categories_table.insert().values(
                event_id=new_event.id, 
                event_category_id=category.id,
            )
            db.execute(event_category)

        for schedule in payload.schedules:
            new_schedule = EventSchedule(
                start_date= schedule.start_date,
                end_date=schedule.end_date,
                event_id=new_event.id,
                description=schedule.description
            )
            db.add(new_schedule)

        return 
    

def get_event_list(payload: BasePaginationFilter) -> list[GetEventOutSchema]:
    with session_scope() as db:
        dto = []

        events = db.query(Event).offset(payload.offset()).limit(payload.size).all()
        for i in range(len(events)):
            dto.append(GetEventOutSchema.from_orm(events[i]))
        
        return dto
    

def get_event(event_id: int) -> GetEventOutSchema:
    with session_scope() as db:
        event = db.query(Event).filter(Event.id == event_id).first()
        return GetEventOutSchema.from_orm(event)