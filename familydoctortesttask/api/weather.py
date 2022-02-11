from datetime import date
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
)

from models.weather import WeatherForecast

from service.weather import WeatherService

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)

@router.get("/", response_model=WeatherForecast)
def get_weather(
    country_code: str,
    city: str,
    date: Optional[date] = None,
    weather_service: WeatherService = Depends(),
):
    return WeatherService.get_weather()

