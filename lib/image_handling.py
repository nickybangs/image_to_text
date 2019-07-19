import config
import numpy as np

# GLOBAL VARIABLES
# img_arr
# components
# sorted_components
# rows
# cols


def get_bounds(itr, context=None):
	img_arr = config.img_arr
	components = config.components
	rows, cols = config.rows, config.cols

	lb, ub, lbr, ubr = components[list(components.keys())[itr]]
	if context != None:
		lb, ub = max(lb - 200*context, 0), min(ub + 200*context, cols)
		lbr, ubr = max(lbr - 30*context, 0), min(ubr + 30*context, rows)
	return lb, ub, lbr, ubr


def draw_box(lb, ub, lbr, ubr, img_copy):
	img_arr = img_copy
	img_arr[lbr:ubr,lb].setfield(0, dtype=np.uint8)
	img_arr[lbr:ubr,ub].setfield(0, dtype=np.uint8)
	img_arr[lbr,lb:ub].setfield(0, dtype=np.uint8)
	img_arr[ubr,lb:ub].setfield(0, dtype=np.uint8)
