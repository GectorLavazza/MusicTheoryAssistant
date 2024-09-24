import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi("design.ui", self)

        self.on_init()

    def on_init(self):
        self.setFixedSize(self.width(), self.height())

        self.exerciseMenu.setHidden(True)
        self.settingsMenu.setHidden(True)

    def build_scale(self, key, scale):
        pass

    def build_chord(self, key, chord, add):
        pass

    def build_interval(self, key, interval):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
