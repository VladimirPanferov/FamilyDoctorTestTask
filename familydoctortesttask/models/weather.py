from datetime import date

from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str
    code: str


class Country(CountryBase):
    id: int

    class Config:
        orm_mode = True


class CityBase(BaseModel):
    name: str


class City(CityBase):
    id: int
    country_id: int

    class Config:
        orm_mode = True


class WeatherForecastBase(BaseModel):
    date: date
    weather: float


class WeatherForecast(WeatherForecastBase):
    id: int
    country_id: int
    city_id: int

    class Config:
        orm_mode = True
