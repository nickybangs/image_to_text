import config
import numpy as np
import os
from fastai.core import Path
from time import time

from image_graph import *
from image_handling import *

pic_name = 'line_41'

im_path = Path('../greek_pages/line_images/LAT_RDR_PG3/')
line_dest = Path('../greek_pages/line_images/')
im_name = pic_name + '.jpeg'
img_arr = get_image_array(im_path/im_name)
fpath = line_dest/f'{pic_name}'
os.system('mkdir -p {}'.format(fpath))
print(fpath)
start = time()
split_lines(img_arr, fpath=fpath)
stop = time()

print((stop - start) / 60)
