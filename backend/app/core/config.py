from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080"
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    class Config:
        case_sensitive = True


settings = Settings()
