import csv

from settings import *


def get_scale(key, scale, notes=NOTES * 2, scales=SCALES):
    res = [key]
    current_index = notes.index(key)
    scale_formula = scales[scale]

    for step in scale_formula[:-1]:
        next_note_index = current_index + step
        res.append(notes[next_note_index])
        current_index += step

    return res


def get_interval(root, interval, notes=NOTES * 2, intervals=INTERVALS):
    current_index = notes.index(root)
    interval_lenght = intervals[interval]

    res = [root, notes[current_index + interval_lenght]]
    return res


def get_chord(root, chord, addition='None', notes=NOTES * 2,
              chords=CHORDS, chord_additions=CHORD_ADDITIONS):
    res = [root]

    if chord not in ('Diminished', 'Augmented') and addition != 'None':
        chord_formula = chords[chord] + chord_additions[addition]
    else:
        chord_formula = chords[chord]

    current_index = notes.index(root)
    print(chord_formula)

    for step in chord_formula:
        next_note_index = current_index + step
        res.append(notes[next_note_index])
        current_index += step

    return res


def get_songs(filename=path + 'resources/dataset.csv', key='0', scale='0', request=''):
    with open(filename, encoding="utf8") as csvfile:
        # откроем csv файл и получим данные
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        data = sorted(reader, key=lambda el: el[5])[:-1][::-1] # отсортируем данные по алфавиту
        possible_songs = [(row[2], row[4]) for row in data if
                          row[10] == key and row[12] == scale]# выберем песни соответствующие введенным данным
        songs = sorted(set(possible_songs))
        res = []
        for song, artist in songs:
            s = f'{song} - {artist}'  # сохраним данные формата ПЕСНЯ - ИСПОЛНИТЕЛЬ в список
            if request in s.lower():
                res.append(s)
        return res
