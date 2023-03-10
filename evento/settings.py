from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Base settings"""

    API_PREFIX: str = "/api"
    ALLOWED_HOST: list[str] = ["*"]

    DATABASE_URL: PostgresDsn

    FASTAPI_KWARGS = {
        "docs_url": f"{API_PREFIX}/docs",
        "redoc_url": f"{API_PREFIX}/redoc",
        "version": "1.0.0",
    }

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    OTP_API_URL: str
    OTP_API_KEY: str

    class Config:
        validate_assignment = True
        env_file = ".env"


settings = Settings()  # type: ignore
