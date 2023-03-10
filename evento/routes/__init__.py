from fastapi.routing import APIRouter
from . import auth, event, user

router = APIRouter()

router.include_router(auth.router, tags=["Auth"], prefix="/auth")
router.include_router(event.router, tags=["Event"], prefix="/event")
router.include_router(user.router, tags=["User"], prefix="/user")
