# -*- coding: utf-8 -*-
import os
import math
from PIL import Image, ImageDraw, ImageFont
from random import random
import uuid
import time
from flask import current_app as app
from app import redis_store

RESULT_REL_DIR = 'static'


def add_name(fn, name, result_fn):
    img = Image.open(fn)
    img_size = img.size

    # font_size = int(img_size[0] * 0.055)
    font_size = int(img_size[0] * 0.07)
    font_file = os.path.join(app.config['RESOURCES_DIR'], 'FZZY.TTF')

    begin_pos = (
        img_size[0] * 0.295,
        img_size[1] * 0.4
    )
    # begin_pos = (
    #     img_size[0] * 0.32,
    #     img_size[1] * 0.40
    # )
    qrcode_pos = (
        int(img_size[0] * 0.7),
        int(img_size[1] * 0.875)
    )

    qrcode_file = Image.open(os.path.join(app.config['IMG_DIR'], 'qrcode.png'))
    img.paste(qrcode_file, qrcode_pos, qrcode_file)
    font = ImageFont.truetype(font_file, font_size)
    draw = ImageDraw.Draw(img)
    draw.text(begin_pos, name + ':', (84, 96, 113), font=font)
    img.save(os.path.join(app.config['STATIC_DIR'], 'results', result_fn))
    return os.path.join(RESULT_REL_DIR, 'results', result_fn)


def get_result_url_by_name_and_id(name, id, pId=None):
    SENTENCES_DIR = os.path.join(app.config['IMG_DIR'], 'sentences', str(id))
    result_fn = str(uuid.uuid1()) + '.png'
    # result_fn = '2.png'
    if pId is not None:
        selected_file = str(pId) + '.png'
        return add_name(os.path.join(SENTENCES_DIR, selected_file), name, result_fn), selected_file.split('.png')[0]
    files = os.listdir(SENTENCES_DIR)
    selected_file = files[int(random() * len(files))]

    print(time.strftime("%Y-%m-%d %X", time.localtime()), ': ', selected_file)
    redis_store.incr('num:totals')

    return add_name(os.path.join(SENTENCES_DIR, selected_file), name, result_fn), selected_file.split('.png')[0]

