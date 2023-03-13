from evento.database import session_scope
from evento.execeptions import UserNotFoundException
from evento.models import LandingForm, User
from evento.types import AddFriendSchema, FormInSchema, UserOutSchema


def add_friend(payload: AddFriendSchema, current_user_id: int) -> UserOutSchema:
    """Add friend and return friend"""
    with session_scope() as db:
        friend = (
            db.query(User)
            .filter(User.phone_number == payload.friend_phone_number)
            .one_or_none()
        )

        if not friend:
            raise UserNotFoundException()

        current_user = db.query(User).filter(User.id == current_user_id).one()

        current_user.friends.append(friend)

        return UserOutSchema.from_orm(friend)


def save_form(payload: FormInSchema) -> None:
    """Add form otherwise raise exception"""

    with session_scope() as db:
        new_form = LandingForm(**payload.dict())

        db.add(new_form)
