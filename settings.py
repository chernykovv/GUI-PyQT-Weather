
import os
import requests

with open(file='.env', mode='r') as file:
    for line in file.readlines():
        key, value = line.split('=')

        os.environ[key] = value


# APP
DEBUG = False

APPLICATIONNAME = 'Weather App'
APPLICATIONVERSION = '0.1.02 (beta)'

# OPENWEATHERMAP
API_KEY = os.environ['API_KEY']

# LOCATION
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
