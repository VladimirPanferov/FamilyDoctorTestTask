from datetime import (
    date,
    datetime,
)
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
    weather_date: Optional[date] = datetime.now().date(),
    weather_service: WeatherService = Depends(),
):
    return weather_service.get(
        country_code=country_code,
        city_name=city,
        weather_date=weather_date,
    )

