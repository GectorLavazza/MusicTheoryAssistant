import librosa
import soundfile as sf
from settings import NOTES

FILES_TO_INTERVALS = {
    'min_sec': 'Minor 2nd',
    'maj_sec': 'Major 2nd',
    'min_third': 'Minor 3rd',
    'maj_third': 'Major 3rd',
    'fourth': '4th',
    'tritone': 'Tritone',
    'fifth': '5th',
    'min_sixth': 'Minor 6th',
    'maj_sixth': 'Major 6th',
    'min_seventh': 'Minor 7th',
    'maj_seventh': 'Major 7th',
    'octave': 'Octave'
}

INTERVALS_TO_FILES = {
    'Minor 2nd': 'min_sec',
    'Major 2nd': 'maj_sec',
    'Minor 3rd': 'min_third',
    'Major 3rd': 'maj_third',
    '4th': 'fourth',
    'Tritone': 'tritone',
    '5th': 'fifth',
    'Minor 6th': 'min_sixth',
    'Major 6th': 'maj_sixth',
    'Minor 7th': 'min_seventh',
    'Major 7th': 'maj_seventh',
    'Octave': 'octave'
}

SCALES_TO_FILES = {
    'Major': 'major_scale',
    'Minor': 'minor_scale',
    'Major Pentatonic': 'major_pentatonic_scale',
    'Minor Pentatonic': 'minor_pentatonic_scale',
    'Blues': 'blues_scale',
    'Dorian': 'dorian_scale'
}

CHORDS_TO_FILES = {
    'Major': 'maj',
    'Minor': 'min',
    'Diminished': 'dim',
    'Augmented': 'aug'
}


def note_shift(semitones, user_id, instrument):
    audio_file = f"data/{instrument}/c_note.mp3"
    y, sr = librosa.load(audio_file)

    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    output_file = f"{user_id}_note.mp3"
    sf.write(output_file, y_shifted, samplerate=sr)


def interval_shift(interval, semitones, user_id, instrument):
    audio_file = f'data/{instrument}/{interval}.mp3'
    y, sr = librosa.load(audio_file)

    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    output_file = f"{user_id}_interval.mp3"
    sf.write(output_file, y_shifted, samplerate=sr)


def get_shifted_scale(scale, root, user_id, instrument):
    audio_file = f'data/{instrument}/{scale}.mp3'
    y, sr = librosa.load(audio_file)

    semitones = NOTES.index(root)

    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    output_file = f"{user_id}_scale.mp3"
    sf.write(output_file, y_shifted, samplerate=sr)


def get_shifted_chord(root, base, user_id, instrument, add=''):
    audio_file = f'data/{instrument}/{base}.mp3'
    if add:
        audio_file = f'data/{instrument}/{base}_{add}.mp3'

    y, sr = librosa.load(audio_file)

    semitones = NOTES.index(root)

    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    output_file = f"{user_id}_chord.mp3"
    sf.write(output_file, y_shifted, samplerate=sr)

