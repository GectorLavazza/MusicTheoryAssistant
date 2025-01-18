from PIL import Image, ImageDraw, ImageFont
import roman
from settings import path


FONT = path + 'resources/arial.ttf'  # путь к файлу шрифта
RESIZED_IMAGE_SIZE = (810, 210)  # размер финального изображения
IMAGE_WIDTH = 1600  # ширина рабочего изображения
IMAGE_HEIGHT = 400  # высота рабочего изображения


def draw_piano(notes_list):
    font = ImageFont.truetype(FONT, 70)  # класс шрифта библиотеки Pillow

    white_key_width = 114
    black_key_width = 57
    black_key_height = IMAGE_HEIGHT * 0.6

    black_key_positions = [85, 199, 427, 541, 655, 883, 997, 1225, 1339, 1453]
    keys = {'C': 0, 'C#\\Db': 1, 'D': 2, 'D#\\Eb': 3, 'E': 4, 'F': 5,
            'F#\\Gb': 6,
            'G': 7, 'G#\\Ab': 8, 'A': 9, 'A#\\Bb': 10,
            'B\\Cb': 11}

    # инициализация изображения
    img = Image.new("RGB",
                    (IMAGE_WIDTH * 2, IMAGE_HEIGHT * 2),
                    "white")
    draw = ImageDraw.Draw(img)

    # рисование клавиш
    for i in range(0, IMAGE_WIDTH * 2, white_key_width * 2):
        draw.rectangle(
            [i, 0, i + white_key_width * 2, IMAGE_HEIGHT * 2],
            fill="white", outline="black")

    for pos in black_key_positions:
        draw.rectangle(
            [pos * 2, 0, (pos + black_key_width) * 2, black_key_height * 2],
            fill="black", outline="black")

    # рисование маркеров нот
    previous_note = notes_list[0]
    current_octave = 1

    for note in notes_list:

        key_pos = keys[note]
        letter = note.split('\\')[0]

        if keys[note] < keys[previous_note] or current_octave == 2:
            current_octave = 2
            key_pos += 14

        if '#' in note:
            x_center = key_pos // 2 * white_key_width * 2 + black_key_width * 4
            y_center = IMAGE_HEIGHT * 0.25 * 2
            circle_radius = 60
            draw.ellipse([x_center - circle_radius, y_center - circle_radius,
                          x_center + circle_radius, y_center + circle_radius],
                         fill="red")
            draw.text((x_center - 42, y_center - 30), letter, fill="white",
                      font=font)
        else:
            x_center = ((key_pos + 1) // 2 *
                        white_key_width * 2 + white_key_width)
            y_center = IMAGE_HEIGHT * 0.75 * 2
            circle_radius = 60
            draw.ellipse([x_center - circle_radius, y_center - circle_radius,
                          x_center + circle_radius, y_center + circle_radius],
                         fill="red")
            draw.text((x_center - 22, y_center - 32), letter, fill="white",
                      font=font)

        previous_note = note

    # изменение размера изображения
    img = img.resize(RESIZED_IMAGE_SIZE)
    return img


def draw_guitar(notes_list):
    font = ImageFont.truetype(FONT, 30)

    strings = 6
    frets = 11

    # все позиции каждой из нот на грифе гитары (указаны лады)
    note_positions = {
        'E': [0, 5, 9, 2, 7, 0],
        'F': [1, 6, 10, 3, 8, 1],
        'F#\\Gb': [2, 7, 11, 4, 9, 2],
        'G': [3, 8, 0, 5, 10, 3],
        'G#\\Ab': [4, 9, 1, 6, 11, 4],
        'A': [5, 10, 2, 7, 0, 5],
        'A#\\Bb': [6, 11, 3, 8, 1, 6],
        'B\\Cb': [7, 0, 4, 9, 2, 7],
        'C': [8, 1, 5, 10, 3, 8],
        'C#\\Db': [9, 2, 6, 11, 4, 9],
        'D': [10, 3, 7, 0, 5, 10],
        'D#\\Eb': [11, 4, 8, 1, 6, 11]
    }

    # расстояние между ладами и между струнами
    fret_spacing = IMAGE_WIDTH / (frets + 1)
    string_spacing = IMAGE_HEIGHT // (strings + 1)

    # инициализация изображения
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')

    draw = ImageDraw.Draw(img)

    # рисование ладов и их нумерация римскими числами
    for i in range(frets):
        x = (i + 1) * fret_spacing
        draw.line([(x, 0), (x, IMAGE_HEIGHT)], fill='gray', width=2)
        font_fret = ImageFont.truetype(FONT, 16)
        draw.text((x - fret_spacing / 2 - 3, 10), roman.toRoman(i),
                  fill='black', font=font_fret)
        if i == frets - 1:
            x = (i + 2) * fret_spacing
            draw.text((x - fret_spacing / 2 - 3, 10), roman.toRoman(i + 1),
                      fill='black', font=font_fret)

    # рисование струн и маркеров нот
    for string_num in range(strings):

        y = (string_num + 1) * string_spacing
        draw.line([(0, y), (IMAGE_WIDTH, y)], fill='black', width=10)

        for note in notes_list:
            note_position = note_positions[note][string_num]
            note_to_draw = note.split('\\')[0]

            if notes_list.index(note) == 0:
                circle_color = 'red'
            else:
                circle_color = 'black'

            x = (note_position + 0.5) * fret_spacing

            circle_radius = 26
            draw.ellipse([(x - circle_radius, y - circle_radius),
                          (x + circle_radius, y + circle_radius)],
                         fill=circle_color)
            if '#' in note:
                x_offset = 32
            else:
                x_offset = 20
            draw.text((x - x_offset / 2, y - 32 / 2), note_to_draw,
                      fill='white',
                      font=font)

    # изменение размера изображения
    img = img.resize(RESIZED_IMAGE_SIZE)
    return img


def draw_isntrument(notes_list, instrument):
    # переход к функциям, генерирующим изображения
    if instrument == 'Piano':
        res = draw_piano(notes_list)
    else:
        res = draw_guitar(notes_list)

    res.save(path + 'resources/curr_image.png')  # сохранение изображения в папке проекта
