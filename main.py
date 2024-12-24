import sys
from email.policy import default

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

        self.build_mode = self.buildTabWidget.tabText(self.buildTabWidget.currentIndex())

        self.instrument = self.sInstrumentCB.currentText()
        self.language = self.sLanguageCB.currentText()

        self.buildButton.clicked.connect(self.build)
        self.searchButton.clicked.connect(self.search)

        self.buildTabWidget.currentChanged.connect(self.set_mode)
        self.buildTabWidget.currentChanged.connect(self.toggle_search)
        self.buildTabWidget.currentChanged.connect(self.clear)
        
        self.cChordCB.currentTextChanged.connect(self.toggle_chord_additions)

        self.notesLW.clear()

        self.sScaleCB.currentTextChanged.connect(self.toggle_search)
        self.sScaleCB.currentTextChanged.connect(self.clear)
        self.sKeyCB.currentTextChanged.connect(self.clear)

        self.cKeyCB.currentTextChanged.connect(self.toggle_search)
        self.cKeyCB.currentTextChanged.connect(self.clear)
        self.cChordCB.currentTextChanged.connect(self.clear)
        self.cAddCB.currentTextChanged.connect(self.clear)

        self.iKeyCB.currentTextChanged.connect(self.clear)
        self.iIntervalCB.currentTextChanged.connect(self.clear)

        self.sApplyButton.clicked.connect(self.apply_settings)
        self.sResetButton.clicked.connect(self.reset_settings)

        self.sInstrumentCB.currentTextChanged.connect(self.toggle_settings_buttons)
        self.sLanguageCB.currentTextChanged.connect(self.toggle_settings_buttons)

        self.songSearchLE.textChanged.connect(self.toggle_search_button)

    def on_init(self):
        self.setFixedSize(self.width(), self.height())

        self.exerciseMenu.setHidden(True)
        self.settingsMenu.setHidden(True)

    def toggle_chord_additions(self):
        if self.cChordCB.currentText() in ('Augmented', 'Diminished'):
            self.cAddCB.setDisabled(True)
            self.cAddCB.setCurrentText('None')
        else:
            self.cAddCB.setEnabled(True)

    def clear(self):
        self.songsLW.clear()
        self.notesLW.clear()

        self.pixmap = QPixmap()
        self.imageView.setPixmap(self.pixmap)

        self.buildButton.setEnabled(True)

    def toggle_search_button(self):
        self.searchButton.setEnabled(True)

    def toggle_settings_buttons(self):
        if (self.sInstrumentCB.currentText() != self.instrument or
                self.sLanguageCB.currentText() != self.language):
            self.sResetButton.setEnabled(True)
            self.sApplyButton.setEnabled(True)
        else:
            self.sResetButton.setDisabled(True)
            self.sApplyButton.setDisabled(True)

    def apply_settings(self):
        self.instrument = self.sInstrumentCB.currentText()
        self.language = self.sLanguageCB.currentText()
        self.sResetButton.setDisabled(True)
        self.sApplyButton.setDisabled(True)

    def reset_settings(self):
        self.sInstrumentCB.setCurrentText(self.instrument)
        self.sLanguageCB.setCurrentText(self.language)

    def toggle_search(self):
        self.songsLW.clear()
        if self.sScaleCB.currentText() not in ('Major', 'Minor'):
            self.searchButton.setDisabled(True)
            self.songSearchLE.setDisabled(True)
        elif self.buildTabWidget.tabText(
            self.buildTabWidget.currentIndex()) != 'Scale':
            self.searchButton.setDisabled(True)
            self.songSearchLE.setDisabled(True)
        else:
            self.searchButton.setEnabled(True)
            self.songSearchLE.setEnabled(True)

    def show_songs(self, key, scale, request):
        k = str(NOTES.index(key))
        s = str(SCALES_TO_NUMBERS[scale])
        songs = get_songs(key=k, scale=s, request=request)
        for i, e in enumerate(songs):
            self.songsLW.insertItem(i, e)

    def show_notes(self, notes):
        self.notesLW.clear()
        for i, e in enumerate(notes, start=0):
            s = str(i + 1) + '. ' + e
            self.notesLW.insertItem(i, s)

    def build_scale(self, key, scale):
        notes = get_scale(key, scale)
        self.show_notes(notes)

        draw_isntrument(notes, self.instrument)
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_chord(self, key, chord, add):
        notes = get_chord(key, chord, add)
        self.show_notes(notes)

        draw_isntrument(notes, self.instrument)
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_interval(self, key, interval):
        notes = get_interval(key, interval)
        self.show_notes(notes)

        draw_isntrument(notes, self.instrument)
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def set_mode(self):
        self.notesLW.clear()
        self.build_mode = self.buildTabWidget.tabText(
            self.buildTabWidget.currentIndex())

    def build(self):
        self.buildButton.setDisabled(True)

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

    def search(self):
        self.searchButton.setDisabled(True)

        key = self.sKeyCB.currentText()
        scale = self.sScaleCB.currentText()

        request = self.songSearchLE.text().lower()

        self.songsLW.clear()
        if scale in ('Major', 'Minor'):
            self.show_songs(key, scale, request)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
