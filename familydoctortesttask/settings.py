from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    weather_api: str
    weather_key: str
    weather_time: Optional[str] = "T12:00"


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
