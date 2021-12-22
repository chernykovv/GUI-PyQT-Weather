
from PyQt5 import QtCore, QtWidgets

from settings import *


class InfoWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        
        self.setObjectName('infoWidget')

        #
        layout = QtWidgets.QVBoxLayout(self)

        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(0)

        appNameLabel = QtWidgets.QLabel(parent=self, text=f'{APPLICATIONNAME.upper()}')
        appNameLabel.setObjectName('appNameLabel')
        appNameLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(appNameLabel)

        appDescriptionLabel = QtWidgets.QLabel(parent=self, text=f'VERSION {APPLICATIONVERSION}')
        appDescriptionLabel.setObjectName('appDescriptionLabel')
        appDescriptionLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(appDescriptionLabel)

