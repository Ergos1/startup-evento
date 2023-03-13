from fastapi.routing import APIRouter
from . import auth, event, user, event_category

router = APIRouter()

router.include_router(auth.router, tags=["Auth"], prefix="/auth")
router.include_router(event.router, tags=["Event"], prefix="/event")
router.include_router(user.router, tags=["User"], prefix="/user")
router.include_router(event_category.router, tags=["EventCategory"], prefix="/event_category")