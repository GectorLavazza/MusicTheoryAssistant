import random
import sys

from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from audio import *


from functions import *
from image_draw import draw_isntrument

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi("design.ui", self)  # загрузка интерфейса

        self.setFixedSize(self.width(), self.height())  # фиксируем размер окна

        self.exerciseMenu.setHidden(True)  # прячем неактивные меню
        self.settingsMenu.setHidden(True)

        self.build_mode = self.buildTabWidget.tabText(
            self.buildTabWidget.currentIndex())  # режим построения зависит от выбранной вкладки

        # получаем инструмент и язык из настроек
        self.instrument = self.sInstrumentCB.currentText()
        self.language = self.sLanguageCB.currentText()

        # подключаем кнопки к функциям, которые будут вызываться при нажатии
        self.buildButton.clicked.connect(self.build)
        self.searchButton.clicked.connect(self.search)

        # подключаем виджет вкладок к функциям, которые будут вызываться при смене вкладки
        self.buildTabWidget.currentChanged.connect(self.set_mode)
        self.buildTabWidget.currentChanged.connect(self.toggle_search)
        self.buildTabWidget.currentChanged.connect(self.clear)

        # подключаем список типов аккордов к функции, которая включает и выключает возможность
        # добавления ступеней к аккорду в зависимости от его типа
        self.cChordCB.currentTextChanged.connect(self.toggle_chord_additions)

        # подключаем переключение возможности поиска и очистку списков песен и нот
        self.sScaleCB.currentTextChanged.connect(self.toggle_search)
        self.sScaleCB.currentTextChanged.connect(self.clear)
        self.sKeyCB.currentTextChanged.connect(self.clear)

        self.cKeyCB.currentTextChanged.connect(self.toggle_search)
        self.cKeyCB.currentTextChanged.connect(self.clear)
        self.cChordCB.currentTextChanged.connect(self.clear)
        self.cAddCB.currentTextChanged.connect(self.clear)

        self.iKeyCB.currentTextChanged.connect(self.clear)
        self.iIntervalCB.currentTextChanged.connect(self.clear)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(100)

        self.listenButton.clicked.connect(self.listen)

        self.clear()  # очистить виджеты построения

        self.all_answers = 0
        self.correct_answers = 0

        self.correct_note = ''
        self.prepare_note()
        self.eNListenButton.clicked.connect(self.listen)
        self.eNSubmitButton.clicked.connect(self.answer_note)
        self.eNNextButton.clicked.connect(self.prepare_note)

        self.correct_interval = ''
        self.eIListenButton.clicked.connect(self.listen)
        self.eISubmitButton.clicked.connect(self.answer_interval)
        self.eINextButton.clicked.connect(self.prepare_interval)

        self.eTabWidget.currentChanged.connect(self.change_exercise)

    def change_exercise(self):
        self.player.stop()
        if self.eTabWidget.currentIndex() == 0:
            self.prepare_note()
        else:
            self.prepare_interval()

    def prepare_note(self):
        self.player.stop()
        self.eNSubmitButton.setEnabled(True)
        self.eNNextButton.setDisabled(True)
        self.eNAnswer.setText('Correct answer: ?')
        self.eNComboBox.clear()
        notes = random.sample(NOTES, 4)
        self.correct_note = random.choice(notes)
        note_shift(self.correct_note, self.instrument)  # получить файл нужного звука
        self.set_player('note.mp3')  # настроить плеер
        for i, n in enumerate(notes):
            self.eNComboBox.insertItem(i, n)

    def answer_note(self):
        self.eNSubmitButton.setDisabled(True)
        self.eNNextButton.setEnabled(True)
        answer = self.eNComboBox.currentText()
        self.all_answers += 1
        if answer == self.correct_note:
            self.eNAnswer.setText(f'Correct answer: {self.correct_note} - your answer is correct!')
            self.correct_answers += 1
        else:
            self.eNAnswer.setText(
                f'Correct answer: {self.correct_note} - your answer is wrong.')
        self.eAvResult.setText(f'Average result: {round(self.correct_answers / self.all_answers * 100, 1)}')

    def prepare_interval(self):
        self.player.stop()
        self.eISubmitButton.setEnabled(True)
        self.eINextButton.setDisabled(True)
        self.eIAnswer.setText('Correct answer: ?')
        self.eIComboBox.clear()
        intervals = random.sample(INTERVALS.keys(), 4)
        self.correct_interval = random.choice(intervals)
        interval_shift(self.correct_interval, random.choice(NOTES), self.instrument)  # получить файл нужного звука
        self.set_player('interval.mp3')  # настроить плеер
        for i, n in enumerate(intervals):
            self.eIComboBox.insertItem(i, n)

    def answer_interval(self):
        self.eISubmitButton.setDisabled(True)
        self.eINextButton.setEnabled(True)
        answer = self.eIComboBox.currentText()
        self.all_answers += 1
        if answer == self.correct_interval:
            self.eIAnswer.setText(f'Correct answer: {self.correct_interval} - your answer is correct!')
            self.correct_answers += 1
        else:
            self.eIAnswer.setText(
                f'Correct answer: {self.correct_interval} - your answer is wrong.')
        self.eAvResult.setText(f'Average result: {round(self.correct_answers / self.all_answers * 100, 1)}')

    def toggle_chord_additions(self):  # выключить добавление ступеней если аккорд не мажорный/минорный
        if self.cChordCB.currentText() in ('Augmented', 'Diminished'):
            self.cAddCB.setDisabled(True)
            self.cAddCB.setCurrentText('None')
        else:
            self.cAddCB.setEnabled(True)

    def listen(self):
        self.player.play()

    def set_player(self, filename):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(100)
        self.player.setSource(QUrl.fromLocalFile(filename))

    def clear(self):  # очистить списки нот и песен и поле для изображения
        self.songsLW.clear()
        self.notesLW.clear()

        self.player.stop()

        self.pixmap = QPixmap()
        self.imageView.setPixmap(self.pixmap)

        self.buildButton.setEnabled(True)
        self.listenButton.setDisabled(True)

    def show_notes(self, notes):  # показать список нот
        self.notesLW.clear()
        for i, e in enumerate(notes, start=0):
            s = str(i + 1) + '. ' + e
            self.notesLW.insertItem(i, s)

    def set_mode(self):
        self.notesLW.clear()
        self.build_mode = self.buildTabWidget.tabText(
            self.buildTabWidget.currentIndex())

    def build(self):  # общая функция построения
        self.buildButton.setDisabled(True)  # выключить кнопку ПОСТРОИТЬ после построения
        self.listenButton.setEnabled(True)

        if self.build_mode == 'Scale':  # построить гамму
            # получение данных из виджетов
            key = self.sKeyCB.currentText()
            scale = self.sScaleCB.currentText()
            self.build_scale(key, scale)  # вызов функции

        elif self.build_mode == 'Chord':  # построить аккорд
            # получение данных из виджетов
            key = self.cKeyCB.currentText()
            chord = self.cChordCB.currentText()
            add = self.cAddCB.currentText()
            self.build_chord(key, chord, add)  # вызов функции

        elif self.build_mode == 'Interval':  # построить интервал
            # получение данных из виджетов
            key = self.iKeyCB.currentText()
            interval = self.iIntervalCB.currentText()
            self.build_interval(key, interval)  # вызов функции

    def build_scale(self, key, scale):
        notes = get_scale(key, scale)  # получить список нот
        self.show_notes(notes)  # показать список нот в виджете

        draw_isntrument(notes, self.instrument)  # создать схему инструмента

        scale_shift(scale, key, self.instrument)  # получить файл нужного звука
        self.set_player('scale.mp3')  # настроить плеер

        # показать изображение в соответствующем виджете
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_chord(self, root, chord, add):
        notes = get_chord(root, chord, add)  # получить список нот
        self.show_notes(notes)  # показать список нот в виджете

        draw_isntrument(notes, self.instrument)  # создать схему инструмента
        chord_shift(chord, root, self.instrument, add)
        self.set_player('chord.mp3')

        # показать изображение в соответствующем виджете
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_interval(self, root, interval):
        notes = get_interval(root, interval)  # получить список нот
        self.show_notes(notes)  # показать список нот в виджете

        interval_shift(interval, root, self.instrument)
        self.set_player('interval.mp3')

        draw_isntrument(notes, self.instrument)  # создать схему инструмента
        # показать изображение в соответствующем виджете
        self.image = QImage('curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def toggle_search_button(self):
        self.searchButton.setEnabled(True)  # сделать кнопку поиска активной

    def toggle_search(self):
        self.songsLW.clear()  # очистить список песен
        if self.sScaleCB.currentText() not in ('Major', 'Minor'):  # отключить возможность поиска если гамма не мажор/минор
            self.searchButton.setDisabled(True)
            self.songSearchLE.setDisabled(True)
        elif self.buildTabWidget.tabText(
                self.buildTabWidget.currentIndex()) != 'Scale': # отключить возможность поиска если режим не SCALE
            self.searchButton.setDisabled(True)
            self.songSearchLE.setDisabled(True)
        else:  # включить возможность поиска
            self.searchButton.setEnabled(True)
            self.songSearchLE.setEnabled(True)

    def show_songs(self, key, scale, request):
        # показать список песен
        k = str(NOTES.index(key))
        s = str(SCALES_TO_NUMBERS[scale])
        songs = get_songs(key=k, scale=s, request=request)
        for i, e in enumerate(songs):
            self.songsLW.insertItem(i, e)  # добавить элементы в список

    def search(self):  # общая функция поиска
        self.searchButton.setDisabled(True)  # отключить кнопку поиска
        # получить данные из виджетов
        key = self.sKeyCB.currentText()
        scale = self.sScaleCB.currentText()
        request = self.songSearchLE.text().lower()
        self.songsLW.clear()
        if scale in ('Major', 'Minor'):
            self.show_songs(key, scale, request)  # показать список песен


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
