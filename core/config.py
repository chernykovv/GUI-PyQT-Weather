
import os
import requests

from .utils import resource


DEBUG = False
UPDATE_TIME = 600_000  # time, in msec

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
def get_current_location():
    '''get current location by ip'''

    response = requests.get('https://ipinfo.io/')
    data = response.json()

    if data:
        return data


location = get_current_location()

CITY = location['city']
COUNTRY = location['country']
LAT, LON = map(float, location['loc'].split(','))
