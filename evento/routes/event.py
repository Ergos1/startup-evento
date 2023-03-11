from fastapi import APIRouter, Depends

from evento.services import (
    create_event,
    get_current_user_id,
    get_event,
    get_event_list,
    subscribe,
)
from evento.types import (
    BasePaginationFilter,
    CreateEventSchema,
    EventOutSchema,
    SubscribeSchema,
)

router = APIRouter()


@router.post("/", response_model=EventOutSchema)
async def create(payload: CreateEventSchema, user_id=Depends(get_current_user_id)):
    return create_event(payload=payload, user_id=user_id)


@router.get(
    "/", response_model=list[EventOutSchema], response_model_exclude={"schedules"}
)
async def list(payload: BasePaginationFilter = Depends()):
    return get_event_list(payload=payload)


@router.get("/{id}", response_model=EventOutSchema)
async def one(id: int):
    return get_event(event_id=id)


@router.post("/subscribe")
async def subscribe_(payload: SubscribeSchema, user_id=Depends(get_current_user_id)):
    return subscribe(payload=payload, user_id=user_id)
