import librosa
import soundfile as sf
from settings import *


# получение ноты
def note_shift(note, instrument):
    audio_file = path + f'resources/data/{instrument}/c_note.mp3'  # путь к аудиофайлу
    y, sr = librosa.load(audio_file)  # превращение файла в массив

    semitones = NOTES.index(note)  # вычисление расстояния сдвига (в полутонах)
    if semitones:  # проверка на случай, если сдвига нет

        # сдвиг высоты звука на указанное расстояние
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    # сохранение файла
    sf.write(path + 'resources/note.mp3', y, samplerate=sr)


# получение интервала
def interval_shift(interval, root, instrument):
    audio_file = path + f'resources/data/{instrument}/{INTERVALS_TO_FILES[interval]}.mp3'
    y, sr = librosa.load(audio_file)

    semitones = NOTES.index(root)
    if semitones:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    sf.write(path + 'resources/interval.mp3', y, samplerate=sr)

# получение гаммы
def scale_shift(scale, key, instrument):
    audio_file = path + f'resources\\data\\{instrument}\\{SCALES_TO_FILES[scale]}.mp3'
    y, sr = librosa.load(audio_file)

    semitones = NOTES.index(key)
    if semitones:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    sf.write(path + 'resources\\scale.mp3', y, samplerate=sr)

# получение аккорда
def chord_shift(chord, root, instrument, add=''):
    audio_file = path + f'resources/data/{instrument}/{CHORDS_TO_FILES[chord]}.mp3'
    if add != 'None':
        # поиск файла аккорда с указанной дополнительной ступенью
        audio_file = path + f'resources/data/{instrument}/{CHORDS_TO_FILES[chord]}_{add}.mp3'

    y, sr = librosa.load(audio_file)

    semitones = NOTES.index(root)
    if semitones:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    sf.write(path + 'resources/chord.mp3', y, samplerate=sr)
