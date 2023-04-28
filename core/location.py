
import json
import os
from dataclasses import dataclass

import requests
from requests.exceptions import RequestException

from .utils import resource
from .exceptions import eprint, LocationServerError


@dataclass
class Location:
    country: str
    city: str
    lat: float
    lon: float

    @classmethod
    def from_ipinfo(cls) -> 'Location':
        '''current location by ip'''

        try:
            response = requests.get('https://ipinfo.io/')
            if response.status_code == 200:
                data = response.json()

                filename = os.path.join('.', 'location.json')
                with open(resource(filename), 'w') as file:
                    json.dump(data, file)

            else:
                raise LocationServerError()

        except (LocationServerError, RequestException) as error:
            eprint(error)

            filename = os.path.join('.', 'location.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    data = json.load(file)

            else:
                data = {
                    'country': 'Russia',
                    'city': 'Novosibirk',
                    'loc': '55.0415,82.9346',
                }

        finally:
            country = data['country']
            city = data['city']
            lat, lon = map(float, data['loc'].split(','))

            return Location(
                country=country,
                city=city,
                lat=lat,
                lon=lon,
            )
