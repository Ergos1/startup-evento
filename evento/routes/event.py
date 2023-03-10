from fastapi import APIRouter

router = APIRouter()


@router.post("/create")
async def create():
    pass


@router.get("/list")
async def list():
    pass


@router.get("/{id}")
async def one():
    pass
