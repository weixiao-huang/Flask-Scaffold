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


def add_name_and_num(fn, name, num, genera, result_fn, flag=0, genera_id=1):
    img = Image.open(fn)
    imgSize = img.size

    numText = 'NO:%06d' % num

    nameLen = len(name.encode('gbk'))
    print(name)

    genera = list(
        genera[(i * 3):(i * 3 + 3)] for i in range(math.ceil(len(genera) / 3))
    )

    generaFontSize = int(imgSize[0] * 0.056)
    fontSize = int(generaFontSize * 1.5)
    fontSize2 = int(fontSize * 0.6)
    numFontSize = int(fontSize * 0.5)
    leftOffset = 0
    numGap = int(fontSize * 0.2)
    gap = int(fontSize * 0.14)
    genera_offset = int(generaFontSize * 0.15)

    if nameLen <= 4 * 2:
        leftOffset = 20
    elif 4 * 2 < nameLen <= 6 * 2:
        leftOffset = 10
        fontSize = int(fontSize * 0.8)
    elif 6 * 2 < nameLen <= 8 * 2:
        fontSize = int(fontSize * 0.65)
        leftOffset = -4
    else:
        fontSize = int(fontSize * 0.5)
        leftOffset = -4
        if nameLen > 10 * 2:
            name = name[:10]
            nameLen = 20

    generaBeginPos = (
        imgSize[0] * 0.715,
        imgSize[1] * 0.015
    )

    numBeginPos = (
        imgSize[0] * 0.18 + leftOffset,
        imgSize[1] * 0.09,
    )
    beginPos = (
        numBeginPos[0] - 5,
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
    GENERA_FONT_FILE = os.path.join(app.config['RESOURCES_DIR'], 'HYTiaoTiaoTiJ.ttf')
    generaFont = ImageFont.truetype(GENERA_FONT_FILE, generaFontSize)
    numFont = ImageFont.truetype(FONT_FILE, numFontSize)
    font = ImageFont.truetype(FONT_FILE, fontSize)
    font2 = ImageFont.truetype(FONT_FILE, fontSize2)

    draw = ImageDraw.Draw(img)
    i = 0
    for item in genera:
        draw.text(
            (generaBeginPos[0], generaBeginPos[1] + (generaFontSize + genera_offset) * i),
            item,
            (80, 80, 80),
            font=generaFont
        )
        i += 1
    draw.text(numBeginPos, numText, (0, 0, 0), font=numFont)
    draw.text(beginPos, name, (0, 0, 0), font=font)
    draw.text(endPos, '同学', (0, 0, 0), font=font2)

    if flag == 1:
        genera_file = os.path.join(app.config['IMG_DIR'], 'genera', '%02d.png' % genera_id)
        genera = Image.open(genera_file)
        img.paste(genera, (0, 0), genera)
    img = img.crop((0, 0, imgSize[0], imgSize[1] * 0.92))
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
    genera_id = int(genera_file[:2])
    select_id = int(random() * 2)
    select_file = selects[select_id]
    result_fn = str(uuid.uuid1()) + '.png'
    print(time.strftime("%Y-%m-%d %X", time.localtime()), ': ', select_file)
    draw_num = int(redis_store.get('num:totals'))
    redis_store.incr('num:totals')
    return add_name_and_num(select_file, name, draw_num, genera_name, result_fn, select_id, genera_id), \
           os.path.join(RESULT_REL_DIR, 'genera', genera_file)
