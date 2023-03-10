from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes
from .settings import settings

app = FastAPI(**settings.FASTAPI_KWARGS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix=settings.API_PREFIX)
