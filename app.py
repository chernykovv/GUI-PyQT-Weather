
import dataclasses
import json
import os
import sys
from pprint import pprint

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from requests.exceptions import RequestException

from core.config import *
from core.exceptions import eprint, WeatherServerError
from core.style import load_style
from core.utils import resource
from core.weather import Weather, WeatherDataCurrent, WeatherDataForecast
from widgets.todayWeatherWidget import TodayWeatherWidget
from widgets.locationWidget import LocationWidget
from widgets.infoWidget import InfoWidget


try:  # change app id for correct icon present
    from PyQt5.QtWinExtras import QtWin

    myAppID = f'{ORGANIZATIONNAME}.{APPLICATIONNAME}.MAINWINDOW.{APPLICATIONVERSION}'
    QtWin.setCurrentProcessExplicitAppUserModelID(myAppID)

except ImportError:
    pass


class UpdateWeatherThread(QtCore.QThread):
    updated = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        weather = Weather.from_openweathermap()
        data = dataclasses.asdict(weather)

        self.updated.emit(data)


class CentralWidget(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()

        #
        layout = QtWidgets.QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(LocationWidget())
        layout.addWidget(TodayWeatherWidget())
        layout.addWidget(InfoWidget())

    def update(self, data: dict):
        weather = Weather.from_dict(data)

        widget = self.findChild(QtWidgets.QWidget, 'todayWeatherWidget')
        widget.update(weather)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, flags):
        super().__init__(flags=flags)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # icon
        icon = QtGui.QIcon(resource('icon.ico'))
        self.setWindowIcon(icon)

        # styles
        style = load_style()
        self.setStyleSheet(style)

        # central widget
        self.centralWidget = CentralWidget()
        self.setCentralWidget(self.centralWidget)

        # update weather thread
        self.updateWeatherThread = UpdateWeatherThread()
        self.updateWeatherThread.updated.connect(self.centralWidget.update)

        # update weather timer
        self.updateWeatherTimer = QtCore.QTimer()
        self.updateWeatherTimer.setInterval(UPDATE_TIME)
        self.updateWeatherTimer.timeout.connect(self.updateWeatherThread.start)
        self.updateWeatherTimer.start()

        QtCore.QTimer.singleShot(300, self.updateWeatherThread.start)

        #
        self.show()

    def mousePressEvent(self, event):
        self._beginPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self._beginPos)
        self.move(
            self.x() + delta.x(),
            self.y() + delta.y(),
        )

        self._beginPos = event.globalPos()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    weather = Weather.from_openweathermap()

    mainWindow = MainWindow(
        flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
    )

    sys.exit(app.exec())
