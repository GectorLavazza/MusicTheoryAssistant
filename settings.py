from os import path
path = path.dirname(__file__) + '/'


NOTES = ['C', 'C#\\Db', 'D', 'D#\\Eb', 'E', 'F',
         'F#\\Gb', 'G', 'G#\\Ab', 'A', 'A#\\Bb', 'B\\Cb']

SCALES = {
    'Major': [2, 2, 1, 2, 2, 2, 1],
    'Minor': [2, 1, 2, 2, 1, 2, 2],
    'Major Pent.': [2, 2, 3, 2, 3],
    'Minor Pent.': [3, 2, 2, 3, 2],
    'Blues': [3, 2, 1, 1, 3, 2],
    'Dorian': [2, 1, 2, 2, 2, 1, 2]
}

INTERVALS = {
    'Minor 2nd': 1, 'Major 2nd': 2,
    'Minor 3rd': 3, 'Major 3rd': 4,
    '4th': 5, 'Tritone': 6, '5th': 7,
    'Minor 6th': 8, 'Major 6th': 9,
    'Minor 7th': 10, 'Major 7th': 11,
    'Octave': 12
}

CHORDS = {
    'Major': [4, 3],
    'Minor': [3, 4],
    'Diminished': [3, 3],
    'Augmented': [4, 4]
}

CHORD_ADDITIONS = {
    'None': '',
    '6': [1], 'maj6': [2],
    '7': [3], 'maj7': [4]
}

INTERVALS_TO_FILES = {
    'Minor 2nd': 'min_sec', 'Major 2nd': 'maj_sec',
    'Minor 3rd': 'min_third', 'Major 3rd': 'maj_third',
    '4th': 'fourth', 'Tritone': 'tritone', '5th': 'fifth',
    'Minor 6th': 'min_sixth', 'Major 6th': 'maj_sixth',
    'Minor 7th': 'min_seventh', 'Major 7th': 'maj_seventh',
    'Octave': 'octave'
}

SCALES_TO_FILES = {
    'Major': 'major_scale', 'Minor': 'minor_scale',
    'Major Pent.': 'major_pentatonic_scale',
    'Minor Pent.': 'minor_pentatonic_scale',
    'Blues': 'blues_scale', 'Dorian': 'dorian_scale'
}

CHORDS_TO_FILES = {
    'Major': 'maj', 'Minor': 'min',
    'Diminished': 'dim', 'Augmented': 'aug'
}

ROMAN = {
    1: 'I.',
    2: 'II.',
    3: 'III.',
    4: 'IV.',
    5: 'V.',
    6: 'VI.',
    7: 'VII.'
}

NOTES_TO_NUMBERS = {
    'C': '0',
    'C#\Db': '1',
    'D': '2',
    'D#\Eb': '3',
    'E': '4',
    'F': '5',
    'F#\Gb': '6',
    'G': '7',
    'G#\Ab': '8',
    'A': '9',
    'A#\Bb': '10',
    'B\Cb': '11'
}

SCALES_TO_NUMBERS = {
    'Major': '1',
    'Minor': '0'
}

DEFAULT_LANGUAGE = 'English'
DEFAULT_INSTRUMENT = 'Piano'

INSTRUMENTS_LIST = ['Piano', 'Guitar']
LANGUAGES_LIST = ['English', 'Русский']
CHORDS_LIST = list(CHORDS.keys())
ADDITIONS_LIST = list(CHORD_ADDITIONS.keys())
SCALES_LIST = list(SCALES.keys())
INTERVALS_LIST = list(INTERVALS.keys())
