
from PyQt5 import QtCore, QtWidgets

from settings import *


class LocationWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
    
        self.setObjectName('locationWidget')

        #
        layout = QtWidgets.QVBoxLayout(self)

        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(0)

        cityLabel = QtWidgets.QLabel(text=CITY, parent=self)
        cityLabel.setObjectName('cityLabel')
        cityLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(cityLabel)

