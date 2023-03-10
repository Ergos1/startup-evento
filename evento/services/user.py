from evento.database import session_scope
from evento.execeptions import UserNotFoundException
from evento.models import User
from evento.types import AddFriendSchema, UserOutSchema


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
