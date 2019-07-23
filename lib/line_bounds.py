from collections import defaultdict
import numpy as np

from support import *
from edge_weighted_digraph import *
from directed_edge import *
from shortest_paths import *


def sign(x, y):
	if x > y:
		return 1
	elif x <= y:
		return -1
	else:
		return 0
	

def get_line_splits(gkarray):
	
	linesums = [g.sum() for g in gkarray]
	LO, HI = min(linesums), max(linesums)
	DELTA = (HI - LO) * .15
	vchanges = defaultdict(list)
	vcvals = defaultdict(list)
	smooth_changes = defaultdict(list)
	velocity = -4
	prev = None
	fundict = {1: min, -1: max}
	for i in range(1, len(linesums)):
		x = linesums[i]
		prev_velocity = velocity
		velocity = sign(x, linesums[i-1])
		if prev_velocity != velocity:
			smooth_changes[velocity].append((i,x))
		if (prev_velocity == velocity) and (smooth_changes != {}) and (velocity != prev):
			if np.abs(np.long(x) - np.long(smooth_changes[velocity][-1][1])) > DELTA:
				vc = fundict[velocity](smooth_changes[velocity], key=lambda x: x[1])
				vchanges[velocity].append(vc[0])
				vcvals[velocity].append(vc[1])
				smooth_changes = defaultdict(list)
				prev = velocity
	_, _, valley_rows, _ = clean_peaks_and_vals(vchanges, vcvals, DELTA)
	return valley_rows


def clean_peaks_and_vals(vchanges, vcvals, DELTA):
	peaks = zip(vchanges[-1], vcvals[-1])
	peaks = [v for v in peaks if v[1] > max(vcvals[-1]) - DELTA*2]
	vchanges[-1] = [p[0] for p in peaks]
	vcvals[-1] = [p[1] for p in peaks]

	line_points = []
	line_vals = []
	for i in range(1, len(vchanges[-1])):
		lb = vchanges[-1][i-1]
		ub = vchanges[-1][i]
		indices = [vchanges[1].index(v) for v in vchanges[1] if v > lb and v < ub]
		minpoint, minval = get_point_and_val(indices, vchanges[1], vcvals[1])
		line_points.append(minpoint)
		line_vals.append(minval)
	
	indices = [vchanges[1].index(v) for v in vchanges[1] if v > vchanges[-1][-1]]
	minpoint, minval = get_point_and_val(indices, vchanges[1], vcvals[1])
	line_points.append(minpoint)
	line_vals.append(minval)

	return vchanges[-1], vcvals[-1], line_points, line_vals


def get_point_and_val(indices, rows, vals):
	if len(indices) > 1:
		min_index = indices[np.argmin(vals[indices[0]:indices[1]+1])]
		minpoint = rows[min_index]
		minval = vals[min_index]
	else:
		minpoint = rows[indices[0]]
		minval = vals[indices[0]]
	return minpoint, minval


def get_line_graph(sub_array):
	cols = sub_array.shape[1]
	rows = sub_array.shape[0]
	num_elems = cols * rows
	s = 0
	t = num_elems + 1
	G = EdgeWeightedDigraph(num_elems + 2, [])

	for i in range(sub_array.shape[0]):
		G.add_edge(DirectedEdge(s, i*cols + 1, np.abs(255-sub_array[i][0])))
		G.add_edge(DirectedEdge((i+1)*cols, t, np.abs(255-sub_array[i][-1])))

	for i in range(rows):
		for j in range(cols-1):
			if (i > 0):
				G.add_edge(DirectedEdge((i*cols)+j + 1, (i-1)*cols + j+2, np.abs(255-sub_array[i-1][j+1])))
			if (i < sub_array.shape[0]-1) and (np.abs(255-sub_array[i+1][j+1]) < 100):
				G.add_edge(DirectedEdge((i*cols)+j + 1, (i+1)*cols + j+2, np.abs(255-sub_array[i+1][j+1])))
			G.add_edge(DirectedEdge((i*cols)+j + 1, i*cols + j+2, np.abs(255-sub_array[i][j+1])))

	return G


def get_sp(G, s=None):

	if s == None:
		s = 0
	t = G.V - 1
	sp = DijsktraSP(G,s)
	e = sp.edge_to[t]
	totalweight = 0
	sp_inds = Stack()
	sp_inds.push(e._to())
	while sp.edge_to[e._from()] != None:
		sp_inds.push(e._from())
		totalweight += e.weight
		e = sp.edge_to[e._from()]

	return sp_inds, totalweight


def get_split_images(sub_array, sp_inds, top, gkarray):

	rows, cols=  sub_array.shape
	sub_array=sub_array.flatten()
	for i in sp_inds.stack[1:]:
		sub_array[i-1] = 260

	newsub=sub_array.reshape((rows, cols))

	col_split = dict()
	for i in sp_inds.stack[1:]:
		col_split[i % cols] = top + (i // cols)

	top_im = []
	bot_im = []

	for i,col in enumerate(gkarray.T):
		top_im.append(col[:col_split[i]])
		bot_im.append(col[col_split[i]:])

	top_pad = max([len(t) for t in top_im])
	bottom_pad = max([len(b) for b in bot_im])

	for i in range(len(top_im)):
		if len(top_im[i]) < top_pad:
			top_im[i] = np.pad(top_im[i], (0, (top_pad-len(top_im[i]))), mode='constant', constant_values=255)
		
	for i in range(len(bot_im)):
		if len(bot_im[i]) < bottom_pad:
			bot_im[i] = np.pad(bot_im[i], ((bottom_pad-len(bot_im[i])),0), mode='constant', constant_values=255)

	return top_im, bot_im
