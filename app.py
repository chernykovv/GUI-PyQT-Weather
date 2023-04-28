
import json
import os
import sys
from pprint import pprint

import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from core.config import *
from core.exception import eprint
from core.utils import resource
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
    updated = QtCore.pyqtSignal(dict, bool)

    def __init__(self):
        super().__init__()

    def run(self):

        try:
            exclude = ','.join(['minutely', 'hourly', 'alerts'])
            units = 'metric'
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&units={units}&exclude={exclude}&appid={API_KEY}'

            response = requests.get(url)

            if response.status_code == 200:
                flag = True
                data = response.json()

                filename = os.path.join('.', 'weather.json')
                with open(resource(filename), 'w') as file:
                    json.dump(data, file)

            else:
                flag = False

        except Exception as error:
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

            self.updated.emit(data, flag)


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

    def update(self, data: dict, flag: bool):

        widget = self.findChild(QtWidgets.QWidget, 'todayWeatherWidget')
        widget.update(data, flag)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, flags):
        super().__init__(flags=flags)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # icon
        icon = QtGui.QIcon(resource('icon.ico'))
        self.setWindowIcon(icon)

        # styles
        filepath = os.path.join('.', 'styles', 'app.css')
        try:
            with open(resource(filepath), mode='r') as file:
                style = file.read()

        except FileNotFoundError as error:
            style = ''
            eprint(error)

        finally:
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

    mainWindow = MainWindow(
        flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
    )

    sys.exit(app.exec())
