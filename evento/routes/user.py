from fastapi import APIRouter, Depends

from evento.services import add_friend, get_current_user, save_form
from evento.types import AddFriendSchema, FormInSchema, UserOutSchema

router = APIRouter()


@router.post(
    "/add-friend",
    response_model=UserOutSchema,
    description="add ```friend``` to user and returns ```friend```",
)
def add_friend_(payload: AddFriendSchema, user_id: int = Depends(get_current_user)):
    return add_friend(payload, user_id)


@router.post("/form", description="save sent landing form")
def save_form_(payload: FormInSchema):
    return save_form(payload=payload)
