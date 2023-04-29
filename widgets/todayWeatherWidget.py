
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets

from core.config import DAY_PARTS
from core.style import load_style
from core.weather import WeatherData, WeatherDataCurrent, WeatherDataForecast


class CurrentWeatherFrame(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName('currentWeatherFrame')

        #
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        iconLabel = QtWidgets.QLabel(text=f'', parent=self)
        iconLabel.setObjectName('iconLabel')
        iconLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(iconLabel)

        temperatureLabel = QtWidgets.QLabel(text=f'', parent=self)
        temperatureLabel.setObjectName('temperatureLabel')
        temperatureLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(temperatureLabel)

        feelsLikeLabel = QtWidgets.QLabel(text=f'', parent=self)
        feelsLikeLabel.setObjectName('feelsLikeLabel')
        feelsLikeLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(feelsLikeLabel)

        # lastUpdatedLabel = QtWidgets.QLabel(text='last updated: Dec 21, 11:44am', parent=self)
        # lastUpdatedLabel.setObjectName('lastUpdatedLabel')
        # lastUpdatedLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # layout.addWidget(lastUpdatedLabel)

    def update(self, data: WeatherDataCurrent, flag: bool):

        if flag:
            # style = [item for item in load_style().split('\n') if item.lstrip(' ').startswith('color: ')]  # FIXME: 
            # reg = re.compile(r'QLabel? {.*?}')
            # text = ''.join([item.strip() for item in style.split('\n')])
            # text = re.findall(r'QLabel? {.*?}', text)[0]
            # re.findall(r'color:? .*?;', text)[0]

            style = 'color: rgb(31, 111, 235)'
        else:
            style = 'color: rgb(160, 160, 160)'

        # iconLabel
        if data.icon is not None:
            filename = os.path.join('.', 'icons', data.icon + '@4x.png')
            pixmap = QtGui.QPixmap(filename)
            pixmap = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)

            iconLabel = self.findChild(QtWidgets.QLabel, 'iconLabel')
            iconLabel.setPixmap(pixmap)
            iconLabel.setStyleSheet(style)

        # temperatureLabel
        temperatureLabel = self.findChild(QtWidgets.QLabel, 'temperatureLabel')
        temperatureLabel.setText(
            f'<strong>{data.t:.0f}</strong> <span>&#8451;</span>'
        )
        temperatureLabel.setStyleSheet(style)

        # feelsLikeLabel
        feelsLikeLabel = self.findChild(QtWidgets.QLabel, 'feelsLikeLabel')
        feelsLikeLabel.setText(
            f'FEELS LIKE: <strong>{data.t_feels_like:.0f}</strong> <span>&#8451;</span>'
        )
        feelsLikeLabel.setStyleSheet(style)


class ForecastWeatherFrame(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName('forecastWeatherFrame')

        #
        self.layout = QtWidgets.QHBoxLayout(self)

        for part in DAY_PARTS:

            frame = QtWidgets.QFrame(self)
            self.layout.addWidget(frame)

            layout = QtWidgets.QVBoxLayout(frame)

            widget = QtWidgets.QLabel(text=f'{part}', parent=self)
            widget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(widget)

            widget = QtWidgets.QLabel(text='', parent=self)
            widget.setObjectName(f'{part}TemperatureLabel')
            widget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(widget)

    def update(self, data: WeatherDataForecast, flag: bool):

        if flag:
            style = 'color: rgb(31, 111, 235)'
        else:
            style = 'color: rgb(160, 160, 160)'

        # 
        for part in DAY_PARTS:
            value = data.t.get(part, {})

            temperatureLabel = self.findChild(QtWidgets.QLabel, f'{part}TemperatureLabel')
            temperatureLabel.setText(
                f'<strong>{value:.0f}</strong> <span>&#8451;</span>'
            )
            temperatureLabel.setStyleSheet(style)


class TodayWeatherWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
    
        self.setObjectName('todayWeatherWidget')

        #
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(0)

        self.layout.addWidget(CurrentWeatherFrame())
        self.layout.addWidget(ForecastWeatherFrame())

    def update(self, data: WeatherData):

        widget = self.findChild(QtWidgets.QFrame, 'currentWeatherFrame')
        widget.update(data.current, data.flag)

        widget = self.findChild(QtWidgets.QFrame, 'forecastWeatherFrame')
        widget.update(data.forecast[0], data.flag)
