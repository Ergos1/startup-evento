from fastapi import APIRouter

router = APIRouter()


@router.post("/me")
async def me():
    pass
