from fastapi import APIRouter, Depends

from evento.models import User
from evento.services import (
    auth_required,
    create_event,
    get_current_user,
    get_event,
    get_event_list,
    subscribe,
)
from evento.types import (
    CreateEventSchema,
    EventListSchema,
    EventOutSchema,
    SubscribeInSchema,
    SubscribeOutSchema,
)

router = APIRouter()


@router.post("/", response_model=EventOutSchema)
@auth_required
async def create(payload: CreateEventSchema, user: User = Depends(get_current_user)):
    return create_event(payload=payload, user=user)


@router.get(
    "/",
    response_model=list[EventOutSchema],
    response_model_exclude={"schedules", "is_subscribed"},
)
async def list(
    payload: EventListSchema = Depends(), user: User = Depends(get_current_user)
):
    return get_event_list(payload=payload, user=user)


@router.get("/{id}", response_model=EventOutSchema)
async def one(id: int, user: User = Depends(get_current_user)):
    return get_event(event_id=id, user=user)


@router.post("/subscribe", response_model=SubscribeOutSchema)
@auth_required
async def subscribe_(
    payload: SubscribeInSchema, user: User = Depends(get_current_user)
):
    return subscribe(payload=payload, user=user)
