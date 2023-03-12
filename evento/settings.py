from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Base settings"""

    API_PREFIX: str = "/api"
    ALLOWED_HOST: list[str] = ["*"]

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOSTNAME: str
    POSTGRES_PORT: int

    FASTAPI_KWARGS = {
        "docs_url": f"{API_PREFIX}/docs",
        "redoc_url": f"{API_PREFIX}/redoc",
        "version": "1.0.0",
    }

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    OTP_API_URL: str
    OTP_API_KEY: str

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOSTNAME}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        validate_assignment = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
print(settings.DATABASE_URL)
