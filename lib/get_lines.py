import numpy as np
from time import time
from imageio import imwrite

from support import *
from edge_weighted_digraph import *
from directed_edge import *
from shortest_paths import *
from line_bounds import *

def sign(x, y):
    if x > y:
        return 1
    elif x <= y:
        return -1
    else:
        return 0



gk = Image.open('/Users/nicholasbangs/Notebooks/personal/greek_reader_master/greek_pages/page_images/GK_RDR_PG3_2.jpeg')
gk = gk.convert('L')
gkarray=np.asarray(gk)
