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

SCALES_TO_FILES = {
    'Major': 'major_scale',
    'Minor': 'minor_scale',
    'Major Pentatonic': 'major_pentatonic_scale',
    'Minor Pentatonic': 'minor_pentatonic_scale',
    'Blues': 'blues_scale',
    'Dorian': 'dorian_scale'
}

INTERVALS = {
    'Minor 2nd': 1,
    'Major 2nd': 2,
    'Minor 3rd': 3,
    'Major 3rd': 4,
    '4th': 5,
    'Tritone': 6,
    '5th': 7,
    'Minor 6th': 8,
    'Major 6th': 9,
    'Minor 7th': 10,
    'Major 7th': 11,
    'Octave': 12
}

CHORDS = {
    'Major': [4, 3],
    'Minor': [3, 4],
    'Diminished': [3, 3],
    'Augmented': [4, 4]
}

CHORD_ADDITIONS = {
    '6': [1],
    'maj6': [2],
    '7': [3],
    'maj7': [4],
    'None': ''
}

ROMAN = {
    1: 'Ⅰ.',
    2: 'Ⅱ.',
    3: 'Ⅲ.',
    4: 'Ⅳ.',
    5: 'Ⅴ.',
    6: 'Ⅵ.',
    7: 'Ⅶ.'
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
