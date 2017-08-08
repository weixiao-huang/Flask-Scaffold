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

def add_name(fn, name, id, result_fn):
    img = Image.open(fn)
    imgSize = img.size

    nameLen = len(name.encode('gbk'))
    print(name)

    print(id)
    fontSize = int(imgSize[0] * 0.08)
    if id == '1':
        beginPos = (
            imgSize[0] * 0.57,
            imgSize[1] * 0.31 - fontSize
        )
    elif id == '2':
        beginPos = (
            imgSize[0] * 0.38,
            imgSize[1] * 0.311 - fontSize
        )
    else:
        beginPos = (
            imgSize[0] * 0.43,
            imgSize[1] * 0.424 - fontSize
        )


    FONT_FILE = os.path.join(app.config['RESOURCES_DIR'], 'font%s.ttf' % id)
    font = ImageFont.truetype(FONT_FILE, fontSize)

    color = (255, 255, 255)
    if id == '1':
        color = (255, 244, 0)
    draw = ImageDraw.Draw(img)
    draw.text(beginPos, name, color, font=font)

    img.save(os.path.join(app.config['STATIC_DIR'], 'results', result_fn))
    return os.path.join(RESULT_REL_DIR, 'results', result_fn)


def get_result_url_by_name(name):
    sentences_dir = app.config['SENTENCES_DIR']
    sentences_files = os.listdir(sentences_dir)
    index = sentences_files[int(random() * len(sentences_files))]

    img_dir = os.path.join(sentences_dir, index)
    img_files = os.listdir(img_dir)
    num = int(random() * len(img_files))

    select_fn = os.path.join(img_dir, img_files[num])
    return add_name(select_fn, name, index, '1.png')
