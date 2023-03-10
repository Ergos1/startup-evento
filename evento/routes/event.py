from fastapi import APIRouter, Depends
from evento.services import get_current_user_id, create_event, get_event_list, get_event, subscribe
from evento.types import CreateEventSchema, BasePaginationFilter, SubscribeSchema

router = APIRouter()


@router.post("/create")
async def create(payload: CreateEventSchema, user_id=Depends(get_current_user_id)):
    return create_event(payload=payload, user_id=user_id)


@router.get("/list")
async def list(payload: BasePaginationFilter):
    return get_event_list(payload=payload)


@router.get("/{id}")
async def one(id: int):
    return get_event(event_id=id)

@router.post("/subscribe")
async def subscribe_(payload: SubscribeSchema, user_id = Depends(get_current_user_id)):
    return subscribe(payload=payload, user_id=user_id)
