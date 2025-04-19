import random
import sys
import json
from settings import path

from PyQt6 import QtWidgets
from PyQt6 import uic
from PyQt6.QtCore import QUrl, QTranslator, QEvent
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

from audio import *
from functions import *
from image_draw import draw_isntrument
from design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)  # загрузка интерфейса

        self.setFixedSize(self.width(), self.height())  # фиксируем размер окна

        self.exerciseMenu.setHidden(True)  # прячем неактивные меню
        self.settingsMenu.setHidden(True)

        self.build_mode = self.buildTabWidget.tabText(
            self.buildTabWidget.currentIndex())  # режим построения зависит от выбранной вкладки

        # получаем инструмент и язык из настроек
        with open(path + 'resources/settings.json', 'r') as file:
            settings = json.load(file)

            self.instrument = settings['instrument']
            self.language = settings['language']

            self.sInstrumentCB.setCurrentIndex(INSTRUMENTS_LIST.index(self.instrument))
            self.sLanguageCB.setCurrentIndex(LANGUAGES_LIST.index(self.language))

        if self.language != 'English':
            self.sLHint.setText('Перезапустите приложение чтобы изменить язык.')

        # подключаем кнопки к функциям, которые будут вызываться при нажатии
        self.buildButton.clicked.connect(self.build)
        self.searchButton.clicked.connect(self.search)

        # подключаем виджет вкладок к функциям, которые будут вызываться при смене вкладки
        self.buildTabWidget.currentChanged.connect(self.toggle_search)
        self.buildTabWidget.currentChanged.connect(self.clear)

        # подключаем список типов аккордов к функции, которая включает и выключает возможность
        # добавления ступеней к аккорду в зависимости от его типа
        self.cChordCB.currentTextChanged.connect(self.toggle_chord_additions)

        # подключаем переключение возможности поиска и очистку списков песен и нот
        self.songSearchLE.textChanged.connect(self.toggle_search_button)
        self.sScaleCB.currentTextChanged.connect(self.toggle_search)
        self.sKeyCB.currentTextChanged.connect(self.toggle_search)
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

        self.eStartButton.clicked.connect(self.prepare_note)

        self.clear()  # очистить виджеты построения

        self.all_answers = 0
        self.correct_answers = 0

        self.correct_note = 0
        self.eNListenButton.clicked.connect(self.listen)
        self.eNSubmitButton.clicked.connect(self.answer_note)
        self.eNNextButton.clicked.connect(self.prepare_note)

        self.correct_interval = 0
        self.eIListenButton.clicked.connect(self.listen)
        self.eISubmitButton.clicked.connect(self.answer_interval)
        self.eINextButton.clicked.connect(self.prepare_interval)

        self.eTabWidget.currentChanged.connect(self.change_exercise)

        # подключаем функции
        self.sApplyButton.clicked.connect(self.apply_settings)
        self.sResetButton.clicked.connect(self.reset_settings)
        self.sInstrumentCB.currentTextChanged.connect(self.toggle_settings_buttons)
        self.sLanguageCB.currentTextChanged.connect(self.toggle_settings_buttons)

        self.set_average()

        self.exerciseMenuButton.clicked.connect(self.clear)

    # включить/выключить кнопки в зависимости от изменений
    def toggle_settings_buttons(self):
        if (INSTRUMENTS_LIST[self.sInstrumentCB.currentIndex()] != self.instrument or
            LANGUAGES_LIST[self.sLanguageCB.currentIndex()] != self.language):
            self.sResetButton.setEnabled(True)
            self.sApplyButton.setEnabled(True)
        else:
            self.sResetButton.setDisabled(True)
            self.sApplyButton.setDisabled(True)

    # применение настроек
    def apply_settings(self):
        self.instrument = INSTRUMENTS_LIST[self.sInstrumentCB.currentIndex()]
        self.language = LANGUAGES_LIST[self.sLanguageCB.currentIndex()]

        settings = {'language': self.language,
                    'instrument': self.instrument}
        with open(path + 'resources/settings.json', 'w') as f:
            json.dump(settings, f)

        self.sResetButton.setDisabled(True)
        self.sApplyButton.setDisabled(True)
        self.clear()
        self.set_average()

    # сброс настроек
    def reset_settings(self):
        self.sInstrumentCB.setCurrentIndex(INSTRUMENTS_LIST.index(self.instrument))
        self.sLanguageCB.setCurrentIndex(LANGUAGES_LIST.index(self.language))

    def change_exercise(self):  # сменить режим упражнений
        self.player.stop()
        if self.eTabWidget.currentIndex() == 0:
            self.prepare_note()
        else:
            self.prepare_interval()

    def prepare_note(self):
        self.player.stop()
        self.eTabWidget.setEnabled(True)
        self.eStartButton.setDisabled(True)
        self.eNSubmitButton.setEnabled(True)  # включить/выключить кнопки
        self.eNNextButton.setDisabled(True)
        msg = 'Правильный ответ: ?' if self.language != 'English' else 'Correct answer: ?'
        self.eNAnswer.setText(msg)  # настроить поле правильного ответа
        self.eNComboBox.clear()
        self.notes = random.sample(NOTES, 4)  # сгенерировать варианты ответов
        self.correct_note = random.randint(0, 3)  # задать правильный ответ
        note_shift(self.notes[self.correct_note], self.instrument)  # получить файл нужного звука
        self.set_player('note.mp3')  # настроить плеер
        for i, n in enumerate(self.notes):  # настроить виджет ответов
            n = self.tr(n) if self.language != 'English' else n
            self.eNComboBox.insertItem(i, n)

    def answer_note(self):
        self.eNSubmitButton.setDisabled(True)  # включить/выключить кнопки
        self.eNNextButton.setEnabled(True)
        answer = self.eNComboBox.currentIndex()  # получить ответ пользователя
        self.all_answers += 1
        # проверить правильность ответа
        correct = self.notes[self.correct_note]
        if answer == self.correct_note:  # верный ответ
            if self.language == 'English':
                msg = f'Correct answer: {correct} - your answer is correct!'
            else:
                msg = f'Правильный ответ: {correct} - ваш ответ верный!'
            self.correct_answers += 1
        else:  # неверный ответ
            if self.language == 'English':
                msg = f'Correct answer: {correct} - your answer is wrong.'
            else:
                msg = f'Правильный ответ: {correct} - ваш ответ неверный.'
        self.eNAnswer.setText(msg)
        self.set_average()

    def set_average(self):
        # изменить средний балл
        if self.all_answers:
            score = round(self.correct_answers / self.all_answers * 100, 1)
        else:
            score = '-'
        if self.language == 'English':
            msg = f'Average result: {score}'
        else:
            msg = f'Средний балл: {score}'
        self.eAvResult.setText(msg)

    def prepare_interval(self):
        self.player.stop()
        self.eTabWidget.setEnabled(True)
        self.eStartButton.setDisabled(True)
        self.eISubmitButton.setEnabled(True)  # включить/выключить кнопки
        self.eINextButton.setDisabled(True)
        msg = 'Правильный ответ: ?' if self.language != 'English' else 'Correct answer: ?'
        self.eIAnswer.setText(msg)  # настроить поле правильного ответа
        self.eIComboBox.clear()
        self.intervals = random.sample(INTERVALS.keys(), 4)  # сгенерировать варианты ответов
        self.correct_interval = random.randint(0, 3)  # задать правильный ответ
        interval_shift(self.intervals[self.correct_interval], random.choice(NOTES), self.instrument)  # получить файл нужного звука
        self.set_player('interval.mp3')  # настроить плеер
        for i, n in enumerate(self.intervals):
            n = self.tr(n) if self.language != 'English' else n
            self.eIComboBox.insertItem(i, n)

    def answer_interval(self):
        self.eISubmitButton.setDisabled(True)  # включить/выключить кнопки
        self.eINextButton.setEnabled(True)
        answer = self.eIComboBox.currentIndex()  # получить ответ пользователя
        self.all_answers += 1  # увеличить число всех ответов
        # проверить правильность
        correct = self.intervals[self.correct_interval]
        if answer == self.correct_interval:  # верный ответ
            if self.language == 'English':
                msg = f'Correct answer: {correct} - your answer is correct!'
            else:
                msg = f'Правильный ответ: {self.tr(correct)} - ваш ответ верный!'
            self.correct_answers += 1
        else:  # неверный ответ
            if self.language == 'English':
                msg = f'Correct answer: {correct} - your answer is wrong.'
            else:
                msg = f'Правильный ответ: {self.tr(correct)} - ваш ответ неверный.'
        self.eIAnswer.setText(msg)
        self.set_average()

    def toggle_chord_additions(self):  # выключить добавление ступеней если аккорд не мажорный/минорный
        if self.cChordCB.currentIndex() not in (0, 1):
            self.cAddCB.setDisabled(True)
            self.cAddCB.setCurrentIndex(0)
        else:
            self.cAddCB.setEnabled(True)

    def listen(self):
        self.player.stop()
        self.player.play()

    def set_player(self, filename):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(100)
        self.player.setSource(QUrl.fromLocalFile(path + f'resources/{filename}'))

    def clear(self):  # очистить списки нот и песен и поле для изображения
        self.songsLW.clear()
        self.notesLW.clear()

        self.player.stop()

        self.pixmap = QPixmap()
        self.imageView.setPixmap(self.pixmap)

        self.buildButton.setEnabled(True)
        self.listenButton.setDisabled(True)

        self.eTabWidget.setDisabled(True)
        self.eStartButton.setEnabled(True)

    def show_notes(self, notes):  # показать список нот
        self.notesLW.clear()
        for i, e in enumerate(notes, start=0):
            s = str(i + 1) + '. ' + e
            self.notesLW.insertItem(i, s)

    def build(self):  # общая функция построения
        self.buildButton.setDisabled(True)  # выключить кнопку ПОСТРОИТЬ после построения
        self.listenButton.setEnabled(True)

        if self.buildTabWidget.currentIndex() == 0:  # построить гамму
            # получение данных из виджетов
            key = NOTES[self.sKeyCB.currentIndex()]
            scale = SCALES_LIST[self.sScaleCB.currentIndex()]
            self.build_scale(key, scale)  # вызов функции

        elif self.buildTabWidget.currentIndex() == 1:  # построить аккорд
            # получение данных из виджетов
            key = NOTES[self.cKeyCB.currentIndex()]
            chord = CHORDS_LIST[self.cChordCB.currentIndex()]
            add = ADDITIONS_LIST[self.cAddCB.currentIndex()]
            self.build_chord(key, chord, add)  # вызов функции

        elif self.buildTabWidget.currentIndex() == 2:  # построить интервал
            # получение данных из виджетов
            key = NOTES[self.iKeyCB.currentIndex()]
            interval = INTERVALS_LIST[self.iIntervalCB.currentIndex()]
            self.build_interval(key, interval)  # вызов функции

    def build_scale(self, key, scale):
        notes = get_scale(key, scale)  # получить список нот
        self.show_notes(notes)  # показать список нот в виджете

        draw_isntrument(notes, self.instrument)  # создать схему инструмента

        scale_shift(scale, key, self.instrument)  # получить файл нужного звука
        self.set_player('scale.mp3')  # настроить плеер

        # показать изображение в соответствующем виджете
        self.image = QImage(path + 'resources/curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_chord(self, root, chord, add):
        print(chord)
        notes = get_chord(root, chord, add)  # получить список нот
        self.show_notes(notes)  # показать список нот в виджете

        draw_isntrument(notes, self.instrument)  # создать схему инструмента
        chord_shift(chord, root, self.instrument, add)
        self.set_player('chord.mp3')

        # показать изображение в соответствующем виджете
        self.image = QImage(path + 'resources/curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def build_interval(self, root, interval):
        notes = get_interval(root, interval)  # получить список нот
        self.show_notes(notes)  # показать список нот в виджете

        interval_shift(interval, root, self.instrument)
        self.set_player('interval.mp3')

        draw_isntrument(notes, self.instrument)  # создать схему инструмента
        # показать изображение в соответствующем виджете
        self.image = QImage(path + 'resources/curr_image.png')
        self.pixmap = QPixmap(self.image)
        self.imageView.setPixmap(self.pixmap)

    def toggle_search_button(self):
        self.searchButton.setEnabled(True)  # сделать кнопку поиска активной

    def toggle_search(self):
        self.songsLW.clear()  # очистить список песен
        if self.sScaleCB.currentIndex() not in (0, 1):  # отключить возможность поиска если гамма не мажор/минор
            self.searchButton.setDisabled(True)
            self.songSearchLE.setDisabled(True)
        elif self.buildTabWidget.currentIndex() != 0: # отключить возможность поиска если режим не SCALE
            self.searchButton.setDisabled(True)
            self.songSearchLE.setDisabled(True)
        else:  # включить возможность поиска
            self.searchButton.setEnabled(True)
            self.songSearchLE.setEnabled(True)

    def show_songs(self, key, scale, request):
        # показать список песен
        k = str(NOTES.index(key))
        songs = get_songs(key=k, scale=str(scale), request=request)
        for i, e in enumerate(songs):
            self.songsLW.insertItem(i, e)  # добавить элементы в список

    def search(self):  # общая функция поиска
        self.searchButton.setDisabled(True)  # отключить кнопку поиска
        # получить данные из виджетов
        key = self.sKeyCB.currentText()
        scale = abs(1 - self.sScaleCB.currentIndex())
        request = self.songSearchLE.text().lower()
        self.songsLW.clear()
        if scale in (0, 1):
            self.show_songs(key, scale, request)  # показать список песен


if __name__ == '__main__':

    import os
    from os import listdir
    from os.path import isfile, join

    print(path)
    # files = [f for f in listdir(path)]
    # print(files)

    try:
        app = QtWidgets.QApplication(sys.argv)

        with open(path + 'resources/settings.json', 'r') as file:
            settings = json.load(file)

            if settings['language'] != 'English':
                translator = QTranslator()
                if translator.load(path + 'resources/translations_ru.qm'):
                    app.installTranslator(translator)

        window = MainWindow()
        window.show()

        app.exec()
    except Exception as e:
        print(e)
        sys.exit()
