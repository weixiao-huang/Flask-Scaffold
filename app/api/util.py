# -*- coding: utf-8 -*-
import os
import math
from PIL import Image, ImageDraw, ImageFont
from random import random
import uuid
import time
from flask import current_app as app

RESULT_REL_DIR = 'static'

draw_num = 0


def add_name_and_num(fn, name, num, genera, result_fn):
    img = Image.open(fn)
    imgSize = img.size

    numText = 'NO:%06d' % num

    nameLen = len(name.encode('gbk'))

    genera = list(
        genera[(i * 3):(i * 3 + 3)] for i in range(math.ceil(len(genera) / 3))
    )

    generaFontSize = 18
    numFontSize = 12
    fontSize = 30
    fontSize2 = 14
    leftOffset = 0
    numGap = 8
    gap = 4

    if nameLen <= 4 * 2:
        leftOffset = 20
    elif 4 * 2 < nameLen <= 6 * 2:
        leftOffset = 10
        fontSize = 24
    elif 6 * 2 < nameLen <= 8 * 2:
        fontSize = 18
    else:
        fontSize = 16
        leftOffset = -4
        if nameLen > 10 * 2:
            name = name[:10]
            nameLen = 20

    generaBeginPos = (
        imgSize[0] * 0.715,
        imgSize[1] * 0.018
    )

    numBeginPos = (
        imgSize[0] * 0.18 + leftOffset,
        imgSize[1] * 0.1,
    )
    beginPos = (
        numBeginPos[0] - 2,
        numBeginPos[1] + numFontSize + numGap,
    )
    endPos = (
        beginPos[0] + fontSize * nameLen / 2 + gap,
        beginPos[1] + fontSize - fontSize2 - 1,
    )

    if len(genera) == 1:
        generaBeginPos = (
            generaBeginPos[0],
            generaBeginPos[1] + generaFontSize * 3 / 2
        )
    elif len(genera) == 2:
        generaBeginPos = (
            generaBeginPos[0],
            generaBeginPos[1] + generaFontSize
        )
    elif len(genera) == 3:
        generaBeginPos = (
            generaBeginPos[0],
            generaBeginPos[1] + generaFontSize / 2
        )

    FONT_FILE = os.path.join(app.config['RESOURCES_DIR'], 'simhei.ttf')
    generaFont = ImageFont.truetype(FONT_FILE, generaFontSize)
    numFont = ImageFont.truetype(FONT_FILE, numFontSize)
    font = ImageFont.truetype(FONT_FILE, fontSize)
    font2 = ImageFont.truetype(FONT_FILE, fontSize2)

    draw = ImageDraw.Draw(img)
    i = 0
    for item in genera:
        draw.text(
            (generaBeginPos[0], generaBeginPos[1] + (generaFontSize + 3) * i),
            item,
            (0, 0, 0),
            font=generaFont
        )
        i += 1
    draw.text(numBeginPos, numText, (0, 0, 0), font=numFont)
    draw.text(beginPos, name, (0, 0, 0), font=font)
    draw.text(endPos, '同学', (0, 0, 0), font=font2)

    img.save(os.path.join(app.config['STATIC_DIR'], 'results', result_fn))
    return os.path.join(RESULT_REL_DIR, 'results', result_fn)


def get_result_url_by_name(name):
    GENERA_FILES = os.listdir(app.config['GENERA_DIR'])
    num = int(random() * len(GENERA_FILES))
    genera_file = GENERA_FILES[num]
    genera_id = genera_file[:2]

    genera_sentences_dir = os.path.join(app.config['SENTENCES_DIR'], genera_id)
    other_sentences_dir = os.path.join(app.config['SENTENCES_DIR'], '00')
    genera_sentence_files = os.listdir(genera_sentences_dir)
    other_sentence_files = os.listdir(other_sentences_dir)
    selects = (
        os.path.join(
            genera_sentences_dir,
            genera_sentence_files[int(random() * len(genera_sentence_files))]
        ),
        os.path.join(
            other_sentences_dir,
            other_sentence_files[int(random() * len(other_sentence_files))]
        )
    )

    genera_name = genera_file[2:-4]
    select_file = selects[int(random() * 2)]
    result_fn = str(uuid.uuid1()) + '.png'
    print(time.strftime("%Y-%m-%d %X", time.localtime()), ': ', select_file)
    return add_name_and_num(select_file, name, 12323, genera_name, result_fn), \
           os.path.join(RESULT_REL_DIR, 'genera', genera_file)
