
import dataclasses
import logging
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from core.config import *
from core.style import load_style
from core.utils import resource
from core.weather import WeatherData, OpenWeatherMapWeatherService
from widgets.todayWeatherWidget import TodayWeatherWidget
from widgets.locationWidget import LocationWidget
from widgets.infoWidget import InfoWidget


try:  # change app id for correct icon present
    from PyQt5.QtWinExtras import QtWin

    myAppID = f'{ORGANIZATIONNAME}.{APPLICATIONNAME}.MAINWINDOW.{APPLICATIONVERSION}'
    QtWin.setCurrentProcessExplicitAppUserModelID(myAppID)

except ImportError:
    pass


WEATHER_SERVICE = OpenWeatherMapWeatherService()


class UpdateWeatherThread(QtCore.QThread):
    updated = QtCore.pyqtSignal(WeatherData)

    def __init__(self):
        super().__init__()

    def run(self):
        data = WEATHER_SERVICE.get()
        self.updated.emit(data)


class CentralWidget(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(LocationWidget())
        layout.addWidget(TodayWeatherWidget())
        layout.addWidget(InfoWidget())

    def update(self, data: WeatherData):
        widget = self.findChild(QtWidgets.QWidget, 'todayWeatherWidget')
        widget.update(data)


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
        self.updateWeatherTimer.setInterval(WEATHER_UPDATE_INTERVAL)
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

    # logger
    if DEBUG:
        logger = logging.getLogger('app')
        logger.debug('app: run.')

    # app
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(
        flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
    )

    sys.exit(app.exec())
