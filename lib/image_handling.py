import config
from fastai.vision import Image, pil2tensor
from PIL import Image as pil_im
import numpy as np
from imageio import imwrite
from line_bounds import *
from shortest_paths import *

# GLOBAL VARIABLES
# img_arr
# components
# sorted_components
# rows
# cols


def get_bounds(itr, context=None):
    '''
    Return the row, col boundaries for the component indexed at itr
    if context != None, it should be an int to specify how much to zoom out
    '''
    img_arr = config.img_arr
    components = config.components
    rows, cols = config.rows, config.cols
    lb, ub, lbr, ubr = components[list(components.keys())[itr]]
    if context != None:
        lb, ub = max(lb - 200*context, 0), min(ub + 200*context, cols)
        lbr, ubr = max(lbr - 30*context, 0), min(ubr + 30*context, rows)
    return lb, ub, lbr, ubr


def draw_box(lb, ub, lbr, ubr, img_copy):
    '''
    Draw a box around the coordinates passed on the image
    '''
    img_arr = img_copy
    img_arr[lbr:ubr,lb].setfield(0, dtype=np.uint8)
    img_arr[lbr:ubr,ub].setfield(0, dtype=np.uint8)
    img_arr[lbr,lb:ub].setfield(0, dtype=np.uint8)
    img_arr[ubr,lb:ub].setfield(0, dtype=np.uint8)


def get_pil_im(im_array):
    '''
    Convert an image array into a PIL image
    '''
    return pil_im.fromarray(im_array).convert("RGB")


def get_fast_im(im_array):
    '''
    Convert an image array into a fastai image
    '''
    return Image(pil2tensor(get_pil_im(im_array), np.float32).div_(255))


def get_sp_from_array(img_arr, s=0, t=None):
    '''
    Returns the pixels for the shortest path from the source to the target
    also returns the total weight of the path.
    source default value is 0
        a dummy vertex representing the source side of the image
    target is G.V - 1
        a dummy vertex representing the target side of the image
    '''
    G = get_line_graph(sub_array)
    if t == None:
        t = G.V-1
    sp = DijkstraSP(G, s)
    return sp.shortest_path(t)


def get_sp_inds_from_vchange(vchanges, img_arr, i, j):
    top, bottom = vchanges[i], vchanges[j]
    sub_array = img_arr[top:bottom, :]
    return get_sp_from_array(sub_array), sub_array, top


def get_inds_and_array(vchanges, img_arr, weight_thresh):
    i, j = 0, 1
    sp_inds, totalweight, sub_array, top = (get_sp_inds_from_vchange(
                                                vchanges, img_arr, i, j))
    while totalweight > weight_thresh:
        i += 1; j += 1
        sp_inds, totalweight, sub_array, top = (get_sp_inds_from_vchange(
                                                vchanges, img_arr, i, j))
    return sp_inds, sub_array, top


def pad_image(im, pad_type, mode='constant', pad_color=255):
    pad = max([len(c) for c in im])
    for i in range(len(im)):
        if len(im[i]) < pad:
            if pad_type=='top':
                pad_range = (0, pad-len(im[i]))
            else:
                pad_range = (pad-len(im[i]), 0)
            im[i] = np.pad(im[i], pad_range, mode=mode, constant_values=pad_color)


def split_lines(img_arr, fpath=None, weight_thresh=np.inf):
    '''
    Takes an image and splits it into its individual lines.
    if fpath is None, it returns a list of images
    else it saves the new images in the directory specified by fpath
    if weight_thresh is set, only splits that have a total weight less than
    the threshold are created
    '''
    imnum = 0
    vchanges = get_line_splits(img_arr)
    sub_ims = []
    while len(vchanges) > 1:
        sp_inds, sub_array, top = (get_inds_and_array(vchanges, img_arr,
                                                weight_thresh))
        top_im, bot_im = get_split_images(*sub_array.shape, sp_inds, top, img_arr)
        line_one = np.array(top_im).T; line_two = np.array(bot_im).T
        if fpath == None:
            sub_ims.append(get_fast_im(np.asarray(line_one)))
        else:
            imwrite(fpath/'line_{}.jpeg'.format(imnum), line_one)

        img_arr = np.asarray(line_two)
        imnum += 1
        vchanges = get_line_splits(img_arr)
    if fpath == None:
        sub_ims.append(get_fast_im(np.asarray(line_one)))
    else:
        imwrite(fpath/'line_{}.jpeg'.format(imnum),line_two)
