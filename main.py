import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage

from image_draw import draw_isntrument
from functions import *


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi("design.ui", self)

        self.on_init()

        self.buildButton.clicked.connect(self.build)
        self.buildTabWidget.currentChanged.connect(self.set_mode)

    def on_init(self):
        self.setFixedSize(self.width(), self.height())

        self.exerciseMenu.setHidden(True)
        self.settingsMenu.setHidden(True)

        self.build_mode = self.buildTabWidget.tabText(self.buildTabWidget.currentIndex())
        self.instrument = 'Guitar'

    def build_scale(self, key, scale):
        print(key, scale)
        notes = get_scale(key, scale)
        draw_isntrument(notes, self.instrument)
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_chord(self, key, chord, add):
        print(key, chord, add)
        notes = get_chord(key, chord, add)
        draw_isntrument(notes, self.instrument)
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_interval(self, key, interval):
        print(key, interval)
        notes = get_interval(key, interval)
        draw_isntrument(notes, self.instrument)
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def set_mode(self):
        self.build_mode = self.buildTabWidget.tabText(
            self.buildTabWidget.currentIndex())

    def build(self):
        if self.build_mode == 'Scale':
            key = self.sKeyCB.currentText()
            scale = self.sScaleCB.currentText()
            self.build_scale(key, scale)

        elif self.build_mode == 'Chord':
            key = self.cKeyCB.currentText()
            chord = self.cChordCB.currentText()
            add = self.cAddCB.currentText()
            self.build_chord(key, chord, add)

        elif self.build_mode == 'Interval':
            key = self.iKeyCB.currentText()
            interval = self.iIntervalCB.currentText()
            self.build_interval(key, interval)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
