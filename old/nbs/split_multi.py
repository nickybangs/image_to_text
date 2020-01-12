import config
from copy import deepcopy
import numpy as np
from PIL import Image as pil_im
from PIL import ImageEnhance
from imageio import imwrite
from itertools import product
import matplotlib.pyplot as plt
from fastai.core import Path
from fastai.vision import load_learner, open_image
from fastai.vision import Image as fast_im
from time import time
import yaml

import dill
import cloudpickle
dill._dill._reverse_typemap['ClassType'] = type

from image_graph import *
from line_bounds import *
from pred_handler import get_top_preds
from image_handling import *

def get_words(letters, space_len=15):
    words = []
    word = []
    i = 1
    while i < len(letters):
        rb = letters[i-1][1]
        lb = letters[i][0]
        if lb - rb > space_len:
            word.append(letters[i-1])
            words.append(word)
            word = []
        else:
            word.append(letters[i-1])
        i += 1
    return words


def get_sp_ims(imarr, frac, nsplits=1):
    i = 0
    rows = imarr.shape[0]
    lefts, rights = [], []
    while i < nsplits:
        lbr = round(i*.125*rows)
        ubr = round((1-i*.125)*rows)
        G = get_line_graph(imarr[lbr:ubr,:])
        source = round(imarr.shape[0] * frac)*imarr.shape[1] + 1
        sp = DijsktraSP(G, source)
        sp_inds, totalweight = sp.shortest_path(G.V - 1) #get_sp(G, s=source)
        #sp_inds.stack.append(source)
        left,right = get_split_images(imarr, sp_inds, 0, imarr) # gets shortest path splits
        lefts.append(get_fast_im(np.asarray(left)))
        rights.append(get_fast_im(np.asarray(right)))
        i += 1
    return lefts, rights


def get_mult(im):
    ip = splitter_model.predict(im)[1][0][1] # get estimated split point
    frac = .5 + round(float(ip),2)
    i1s, i2s = split_parts(im, frac, nsplits=4) # gets straight line split
    lefts, rights = get_sp_ims(np.asarray(im.data[0]).T, 3)
    return (lefts, rights), (i1, i2)


# gets the sub-letters generated by the two split methods with the higher score
def get_best_letters(sp_splits, mdl_splits):
    sp1 = get_top_preds(sp_splits[0], top=3)
    sp2 = get_top_preds(sp_splits[1], top=3)
    md1 = get_top_preds(mdl_splits[0], top=3)
    md2 = get_top_preds(mdl_splits[1], top=3)
    sp_score = sp1[0][1] * sp2[0][1]
    md_score = md1[0][1] * md2[0][1]
    if sp_score > md_score:
        return (sp1, sp_splits[0]), (sp2, sp_splits[1])
    else:
        return (md1, mdl_splits[0]), (md2, mdl_splits[1])


# use the predicted split-point to return the two sub-characters
def split_parts(img, split_frac, nsplits=1):
    left_im = img.data[:,:,:int(img.data.shape[2]*split_frac)+1]
    right_im = img.data[:,:,int(img.shape[2]*split_frac):]
    left_ims, right_ims = [fast_im(left_im)], [fast_im(right_im)]
    i = 1
    while i < nsplits:
        rand_l = np.random.uniform(low=split_frac/2, high=split_frac)
        rand_r = np.random.uniform(low=split_frac, high=split_frac + (1 - split_frac)/2)
        for sp in [rand_l, rand_r]:
            left_ims.append(fast_im(img.data[:,:,:int(img.data.shape[2]*sp)+1]))
            right_ims.append(fast_im(img.data[:,:,int(img.shape[2]*sp):]))
        i += 1
    return left_ims, right_ims


# if the two characters are within 10 pxls of eachother, place them next to each other, else add a space
def add_letter(ltrs, lbound, rbound):
    l = ''
    if rbound - lbound > 10:
        l += ' '
    return l + '/'.join([lm_inv[l] for l in ltrs])


def filter_letters(word):
    return [ltr for ltr in word if ltr[2][0][0][0] not in lang_model_skip]