import os
from PIL import Image, ImageDraw, ImageFont
import uuid
import time
from random import random
from flask import current_app as app

RESULT_REL_DIR = 'static'


def get_pos_by_baseline(fontSize, width, nameeLen, right=False, gap=0):
    if right:
        return width - int((fontSize / 2 + gap) * nameeLen)
    else:
        return width - int((fontSize / 2 + gap) * nameeLen / 2)


def add_name(fn, name, result_fn, pId):
    img = Image.open(fn)
    imgSize = img.size

    nameLen = len(name.encode('gbk'))

    fn = os.path.join(app.config['RESOURCES_DIR'], 'FZZY.TTF')
    tip_fn = os.path.join(app.config['RESOURCES_DIR'], 'PingFang Light.ttf')

    fontSize = int(imgSize[0] * 0.079)
    tipFontSize = int(imgSize[0] * 0.04)

    if pId == '1':
        begin_pos = (
            get_pos_by_baseline(fontSize, imgSize[0] * 0.50, nameLen),
            imgSize[1] * 0.192,
        )
    elif pId == '2':
        begin_pos = (
            get_pos_by_baseline(fontSize, imgSize[0] * 0.25, nameLen),
            imgSize[1] * 0.312,
        )
    elif pId == '3':
        begin_pos = (
            get_pos_by_baseline(fontSize, imgSize[0] * 0.50, nameLen),
            imgSize[1] * 0.3,
        )
    elif pId == '4':
        begin_pos = (
            imgSize[0] * 0.555,
            imgSize[1] * 0.28,
        )
    elif pId == '5':
        if nameLen > 8:
            fontSize = int(fontSize * 0.8)
            begin_pos = (
                get_pos_by_baseline(fontSize, imgSize[0] * 0.49, nameLen),
                imgSize[1] * 0.2,
            )
        else:
            begin_pos = (
                get_pos_by_baseline(fontSize, imgSize[0] * 0.50, nameLen),
                imgSize[1] * 0.192,
            )

    font = ImageFont.truetype(fn, fontSize)
    tip_font = ImageFont.truetype(tip_fn, tipFontSize)

    tip = '长按扫码'
    tipLen = len(tip.encode('gbk'))
    qrcode_size = int(imgSize[0] * 0.2)
    tip_pos = (
        int(imgSize[0] * 0.75),
        int(imgSize[1] * 0.95)
    )
    qrcode_pos = (
        tip_pos[0] - qrcode_size // 2 + int(tipLen * tipFontSize / 4),
        tip_pos[1] - qrcode_size
    )

    qrcode_file = Image.open(
            os.path.join(app.config['IMG_DIR'], 'sports', 'qrcode.png')
        ).resize((qrcode_size, qrcode_size), Image.ANTIALIAS)
    img.paste(qrcode_file, qrcode_pos, qrcode_file)

    draw = ImageDraw.Draw(img)
    draw.text((begin_pos[0], begin_pos[1]), name, (0, 0, 0), font=font)
    draw.text(tip_pos, tip, (114, 114, 114), font=tip_font)
    img.save(os.path.join(app.config['STATIC_DIR'], 'results', result_fn))

    return os.path.join(RESULT_REL_DIR, 'results', result_fn), img.convert('RGB').getpixel((10, 10))


def get_result_url_by_name(name):
    SENTENCES_DIR = os.path.join(app.config['IMG_DIR'], 'sports')
    result_fn = str(uuid.uuid1()) + '.png'

    # pId = str(int(random() * 4) + 1)
    dir_path = os.path.join(SENTENCES_DIR, 'sentences')
    files = os.listdir(dir_path)
    index = int(random() * len(files))
    selected_file = files[index]
    pId = selected_file.split('-')[0]
    print(time.strftime("%Y-%m-%d %X", time.localtime()), ': ', selected_file)

    return add_name(os.path.join(dir_path, selected_file), name, result_fn, pId)
