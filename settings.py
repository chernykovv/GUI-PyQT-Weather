
import os

with open(file='.env', mode='r') as file:
    for line in file.readlines():
        key, value = line.split('=')

        os.environ[key] = value


#
DEBUG = False

APPLICATIONNAME = 'Weather App'
APPLICATIONVERSION = '0.1.01 (beta)'

API_KEY = os.environ['API_KEY']
LAT, LON = 54.9833, 82.8964
CITY = 'Novosibirsk'

