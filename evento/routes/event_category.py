from fastapi import APIRouter, Depends


from evento.services import (
    get_event_category_list,
)
from evento.types import (
    EventCategoryListSchema,
    BasePaginationFilter,
)

router = APIRouter()

@router.get("/", response_model=list[EventCategoryListSchema])
async def list(payload: BasePaginationFilter = Depends()):
    return get_event_category_list(payload=payload)