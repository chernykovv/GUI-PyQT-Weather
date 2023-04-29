
import os

from .location import IpInfoLocationService
from .utils import resource


DEBUG = False


# --------        ENV        --------
filepath = '.env'
with open(resource(filepath), mode='r') as file:
    for line in file.readlines():
        key, value = line.split('=')

        os.environ[key] = value

API_KEY = os.environ['API_KEY']  # openweathermap API_KEY


# --------        APP        --------
ORGANIZATIONNAME = 'Exinker'
APPLICATIONNAME = 'Weather App'
APPLICATIONVERSION = '0.2.4 (alpha)'


# --------        LOCATION        --------
LOCATION = IpInfoLocationService().get()

# --------        WEATHER        --------
WEATHER_UPDATE_INTERVAL = 600_000  # time, in msec
DAY_PARTS = ('morning', 'day', 'evening', 'night', )
