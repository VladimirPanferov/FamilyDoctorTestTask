from sqlalchemy import (
    Column,
    Date,
    Integer,
    ForeignKey,
    String,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey("countries.id"), index=True)
    name  = Column(String, unique=True)
    code = Column(String, unique=True)

    country = relationship("Country", backref="cities")


class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey("countries.id"), index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), index=True)
    date = Column(Date)
    weather = Column(Integer)

    country = relationship("Country", backref="countries")
    city = relationship("City", backref="cities")
