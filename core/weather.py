
import json
import logging
import os
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass

import requests
from requests.exceptions import RequestException

from .config import LOCATION, API_KEY, DEBUG, DAY_PARTS
from .utils import resource
from .exceptions import eprint, WeatherServerError


@dataclass
class WeatherDataCurrent:
    icon: str | None
    t: float
    t_feels_like: float

    def __str__(self) -> str:
        return f'{self.icon}, {self.t}, C'


@dataclass
class WeatherDataForecast:
    t: Mapping[str, float]
    t_feels_like: Mapping[str, float]


@dataclass
class WeatherData:
    flag: bool
    current: WeatherDataCurrent
    forecast: tuple[WeatherDataForecast]


class WeatherService(ABC):
    '''Interface to get weather data from any service'''

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Mapping) -> WeatherData:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> WeatherData:
        raise NotImplementedError


class OpenWeatherMapWeatherService:
    mapping = {
        'morning': 'morn',
        'day': 'day',
        'evening': 'eve',
        'night': 'night',
    }

    @classmethod
    def from_dict(cls, data: Mapping) -> WeatherData:
        return WeatherData(
            flag=data['flag'],
            current=WeatherDataCurrent(**data['current']),
            forecast=tuple(WeatherDataForecast(**datum) for datum in data['forecast']),
        )

    def get(self) -> WeatherData:

        def _convert_dat(dat: Mapping):
            return {
                key: dat[self.mapping[key]]
                for key in DAY_PARTS
            }

        try:
            exclude = ','.join(['minutely', 'hourly', 'alerts'])
            units = 'metric'
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={LOCATION.lat}&lon={LOCATION.lon}&units={units}&exclude={exclude}&appid={API_KEY}'

            response = requests.get(url)
            if response.status_code == 200:
                flag = True
                data = response.json()

                filename = os.path.join('.', '.weather.json')
                with open(resource(filename), 'w') as file:
                    json.dump(data, file)

            else:
                raise WeatherServerError()

        except (RequestException, WeatherServerError) as error:
            eprint(error)

            filename = os.path.join('.', '.weather.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    data = json.load(file)
            else:
                data = {}

            flag = False

        #
        current = WeatherDataCurrent(
            icon=data['current']['weather'][0]['icon'],
            t=data['current']['temp'],
            t_feels_like=data['current']['feels_like'],
        )
        forecast=tuple([
            WeatherDataForecast(
                t=_convert_dat(datum['temp']),
                t_feels_like=_convert_dat(datum['feels_like']),
            )
            for datum in data['daily']
        ])

        #
        logger = logging.getLogger('app')
        logger.info('Weather: {}'.format(
            f'Weather: {current}' if flag else 'Weather: service error!',
        ))

        #
        return WeatherData(
            flag=flag,
            current=current,
            forecast=forecast,
        )
