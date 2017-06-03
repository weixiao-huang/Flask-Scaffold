# -*- coding: utf-8 -*-
import os
import math
from PIL import Image, ImageDraw, ImageFont
from random import random
import uuid
import time
from flask import current_app as app

RESULT_REL_DIR = 'static'


def add_name(fn, name, result_fn, flag):
    img = Image.open(fn)
    imgSize = img.size

    font_size = int(imgSize[0] * 0.084)

    beginPos = (
        imgSize[0] * 0.11,
        imgSize[1] * 0.13
    )

    if flag == 2:
        beginPos = (
            imgSize[0] * 0.062,
            imgSize[1] * 0.25
        )

    FONT_FILE = os.path.join(app.config['RESOURCES_DIR'], 'simhei.ttf')

    font = ImageFont.truetype(FONT_FILE, font_size)
    draw = ImageDraw.Draw(img)
    draw.text(beginPos, name, (255, 255, 255), font=font)

    img.save(os.path.join(app.config['STATIC_DIR'], 'results', result_fn))
    return os.path.join(RESULT_REL_DIR, 'results', result_fn)


def get_img_by_name(name):
    SENTENCES_DIR = os.path.join(app.config['IMG_DIR'], 'sentences')

    selected_folder = int(random() * 2) + 1

    files_dir = os.path.join(SENTENCES_DIR, str(selected_folder))
    files = os.listdir(files_dir)
    selected_file = files[int(random() * len(files))]

    result_fn = str(uuid.uuid1()) + '.png'

    return add_name(os.path.join(files_dir, selected_file), name, result_fn, selected_folder)
