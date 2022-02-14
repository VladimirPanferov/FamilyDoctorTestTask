from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    weather_api: str
    weather_key: str
    weather_time: Optional[str] = "12:00"

    database_url: str


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
