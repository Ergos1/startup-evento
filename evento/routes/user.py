from fastapi import APIRouter, Depends

from evento.services import add_friend, get_current_user_id
from evento.types import AddFriendSchema, UserOutSchema

router = APIRouter()


@router.post("/me")
async def me():
    pass


@router.post("/add-friend", response_model=UserOutSchema)
def add_friend_(payload: AddFriendSchema, user_id: int = Depends(get_current_user_id)):
    return add_friend(payload, user_id)
