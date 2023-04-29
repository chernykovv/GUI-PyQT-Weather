
import logging
import logging.config
import os

from .location import IpInfoLocationService
from .utils import resource


DEBUG = True


# --------        LOGGING        --------
logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'stream_formatter': {
            'format': '[%(asctime)s: %(levelname)s] %(message)s',
        },
        'file_formatter': {
            'format': '[%(asctime)s: %(levelname)s] %(message)s',
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'stream_formatter',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'level': logging.INFO,
            'filename': os.path.join('.', 'app.log'),
            'mode': 'a',
            'formatter': 'file_formatter',
        },
    },

    'loggers': {
        'app': {
            'level': logging.DEBUG,
            'handlers': ['stream_handler', 'file_handler'],
            'propagate': True,
        },
    },

}

logging.config.dictConfig(logger_config)


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
