import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("MusicTheoryApp.ui", self)
        self.setFixedSize(self.width(), self.height())

        self.windows = {
            'build': self.Build,
            'train': self.Training,
        }

        self.current_window = 'build'

        for window in self.windows:
            if window != 'build':
                self.windows[window].setVisible(False)
                self.windows[window].setEnabled(False)
        self.windows['build'].setVisible(True)
        self.windows['build'].setEnabled(True)

        self.trainMenuButton.clicked.connect(self.switch_window)
        self.buildMenuButton.clicked.connect(self.switch_window)

    def switch_window(self):
        sender = self.sender()
        switch_to = sender.text().lower()
        for window in self.windows:
            if window != switch_to:
                self.windows[window].setVisible(False)
                self.windows[window].setEnabled(False)
        self.windows[switch_to].setVisible(True)
        self.windows[switch_to].setEnabled(True)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
