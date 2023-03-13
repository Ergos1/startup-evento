from evento.database import session_scope
from evento.models import EventCategory
from evento.types import (
    BasePaginationFilter,
    EventCategoryListSchema,
)

def get_event_category_list(payload: BasePaginationFilter) -> list[EventCategoryListSchema]:
    """Return list of event categories, with option to use searchText"""
    
    with session_scope() as db:
        event_categories = db.query(EventCategory).filter(EventCategory.name.contains(payload.search_text)).offset(payload.offset()).limit(payload.limit).all()
        return [EventCategoryListSchema.from_orm(event_category) for event_category in event_categories]