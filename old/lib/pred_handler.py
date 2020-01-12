from fastai.vision import open_image
from imageio import imwrite
import os
import config
from image_handling import *
from file_maintenance import *

# GLOBAL VARIABLES
# model
# letter_dict
# letter_dest
# img_arr
# components


def get_top_preds(im, imtype='file', top=3):
    if imtype == 'file':
        img = open_image(im)
    else:
        img = im
    model = config.model
    raw_preds = model.predict(img)[2]
    classes = model.data.classes
    zipped = list(zip(classes, raw_preds))
    sorted_preds = sorted(zipped, key=lambda x: x[1], reverse=True)
    return sorted_preds[:top]


def preprocess():
    letter_dict = config.letter_dict
    img_arr = config.img_arr
    model = config.model
    components = config.components
    letter_dest = config.letter_dest
    temp_path = config.temp_path

    autotag_pth = letter_dest/'auto_tags'
    new_components = dict()

    for k in components:
        lb, ub, lbr, ubr = components[k]
        imname = temp_path/'temp_letter.jpg'
        try:
            imwrite(imname, img_arr[lbr:ubr,lb:ub])
        except:
            print(lbr,ubr,lb,ub)
        preds = get_top_preds(imname, 1)
        if preds[0][1] > .85:
            ltr = preds[0][0]
            ltrpath = autotag_pth/ltr
            os.system('mkdir -p {}'.format(ltrpath))
            next_id = get_next_ind(ltr)
            prob = int(100*preds[0][1])
            new_imname = '{0}_{1}_{2}_{3}.jpg'.format(ltr, next_id, k, prob)
            os.system('mv {0} {1}'.format(imname, ltrpath/new_imname))
        else:
            new_components[k] = components[k]
    config.new_components = new_components
