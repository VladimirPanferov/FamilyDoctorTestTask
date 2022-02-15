from unicodedata import name
import requests
import datetime

from typing import Optional, Tuple, Union

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

import tables

from database import get_session


from familydoctortesttask.settings import settings


TIME = datetime.time(*map(int, settings.weather_time.split(":")))
MOSCOW_TZ = MOSCOW_TZ = datetime.timezone(datetime.timedelta(hours=3))


class WeatherService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get(
        self,
        country_code: str,
        city_name: str,
        weather_date: Optional[datetime.date] = None,
    ):

        weather = self._get_weather_from_db(
            country_code=country_code,
            city_name=city_name,
            weather_date=weather_date,
        )
        if weather:
            return weather

        weather_forecast = WeatherService._get_weather_from_api(
            country_code,
            city_name,
            weather_date,
        )
        print(weather_forecast)
        return self._create(
            **weather_forecast
        )

    def _create(
        self,
        country_code: str,
        city_name: str,
        weather_forecast: float,
        weather_date: Optional[datetime.datetime] = None
    ):
        country = self._get_country(country_code=country_code)
        city = self._get_city(city_name=city_name)
        if city:
            city_id = city.id
        else:
            if country:
                country_id = country.id
            else:
                country_id = self._create_country(
                    country_code=country_code
                )
            city_id = self._create_city(
                country_id=country_id,
                city_name=city_name
            )
        
        return self._create_weather_forecast(
            country_id=country_id,
            city_id=city_id,
            weather_date=weather_date,
            weather_forecast=weather_forecast,
        )

    def _create_country(self, country_code: str) -> int:
        country = tables.Country(
            name=country_code,
            code=country_code,
        )
        self.session.add(country)
        self.session.commit()
        return country.id
    
    def _create_city(self, country_id: Union[Tuple[int], int], city_name: str) -> int:
        city = tables.City(
            country_id=country_id,
            name=city_name,
        )
        self.session.add(city)
        self.session.commit()
        return city.id

    def _create_weather_forecast(
        self,
        country_id: int,
        city_id: int,
        weather_date: datetime.datetime,
        weather_forecast: int
    ):
        forecast = tables.WeatherForecast(
            country_id=country_id,
            city_id=city_id,
            date=weather_date,
            weather=weather_forecast,
        )
        self.session.add(forecast)
        self.session.commit()
        return forecast

    def _get_country(self, country_code: str):
        country = (
            self.session
            .query(tables.Country)
            .filter(tables.Country.code == country_code)
            .first()
        )
        return country

    def _get_city(self, city_name: str):
        city = (
            self.session
            .query(tables.City)
            .filter(tables.City.name == city_name)
            .first()
        )
        return city

    def _get_weather_from_db(
        self,
        country_code: str,
        city_name: str,
        weather_date: Optional[datetime.date] = None,
    ):
        target_date = WeatherService._get_target_date(
            weather_date=weather_date)
        weather_forecast = (
            self.session
            .query(tables.WeatherForecast)
            .join(
                tables.City,
                tables.City.id == tables.WeatherForecast.city_id,
                isouter=True,
            )
            .join(
                tables.Country,
                tables.Country.id == tables.WeatherForecast.country_id,
                isouter=True,
            )
            .filter(
                tables.Country.code == country_code,
                tables.City.name == city_name,
                tables.WeatherForecast.date == target_date,
            )
            .first()
        )
        return weather_forecast

    @staticmethod
    def _get_weather_from_api(
        country_code: str,
        city: str,
        weather_date: Optional[datetime.date] = None
    ):
        parameters = {
            "q": f"{city},{country_code}",
            "units": "metric",
            "exclude": "alerts, daily",
            "appid": settings.weather_key,
        }

        response = requests.get(
            settings.weather_api,
            params=parameters,
        )
        response.raise_for_status()
        data = response.json()
        target_date = WeatherService._get_target_date(
            weather_date=weather_date,
        )
        timestamp = int(datetime.datetime.timestamp(target_date))
        for weather in filter(lambda x: x["dt"] == timestamp, data["list"]):
            return {
                "country_code": country_code,
                "city_name": city,
                "weather_date": target_date,
                "weather_forecast": weather["main"]["temp"],
            }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _get_target_date(weather_date: Optional[datetime.date] = None) -> datetime.datetime:
        if weather_date is None:
            now = datetime.datetime.now(tz=MOSCOW_TZ)
            target_date = datetime.datetime.combine(
                date=now.date(),
                time=TIME,
                tzinfo=MOSCOW_TZ
            )
            return target_date
        target_date = datetime.datetime.combine(
            date=weather_date,
            time=TIME,
            tzinfo=MOSCOW_TZ
        )
        return target_date
