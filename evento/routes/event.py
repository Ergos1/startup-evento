from fastapi import APIRouter, Depends

from evento.services import create_event, get_current_user_id, get_event, get_event_list
from evento.types import BasePaginationFilter, CreateEventSchema

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
