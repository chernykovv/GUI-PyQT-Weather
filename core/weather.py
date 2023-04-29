
import json
import os
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


@dataclass
class WeatherDataForecast:
    t: Mapping[str, float]
    t_feels_like: Mapping[str, float]


@dataclass
class Weather:
    flag: bool
    current: WeatherDataCurrent
    forecast: tuple[WeatherDataForecast]

    @classmethod
    def from_dict(cls, data) -> 'Weather':

        return Weather(
            flag=data['flag'],
            current=WeatherDataCurrent(**data['current']),
            forecast=tuple(
                WeatherDataForecast(**datum)
                for datum in data['forecast']
            ),
        )

    @classmethod
    def from_openweathermap(cls) -> 'Weather':
        MAPPING = {
            'morning': 'morn',
            'day': 'day',
            'evening': 'eve',
            'night': 'night',
        }

        def _convert_dat(dat: dict):
            return {
                key: dat[MAPPING[key]]
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

                filename = os.path.join('.', 'weather.json')
                with open(resource(filename), 'w') as file:
                    json.dump(data, file)

            else:
                raise WeatherServerError()

        except (RequestException, WeatherServerError) as error:
            eprint(error)

            filename = os.path.join('.', 'weather.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    data = json.load(file)
            else:
                data = {}

            flag = False

        finally:
            if DEBUG:
                pprint(data)

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

            return cls(
                flag=flag,
                current=current,
                forecast=forecast,
            )
