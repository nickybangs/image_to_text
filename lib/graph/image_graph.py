from support import UF
from edge_weighted_digraph import EdgeWeightedDigraph as Graph
from directed_edge import DirectedEdge as Edge
import numpy as np
from PIL import Image
from collections import defaultdict
import config


def get_image_array(impath):
	
	image_array = Image.open(impath)
	image_array = image_array.convert('L')
	return np.asarray(image_array)


def get_graph(path, fname, impath, save_graph=True):
	'''creates a graph if one does not exist for the provided image'''

	image_array = get_image_array(impath)
	rows, cols = image_array.shape
	num_elems = rows * cols

	if path/fname in path.ls():
		G = Graph.from_filename(str(path/fname))
	else:
		imrows = [[j for i in range(cols)] for j in range(rows)]
		colrows = [[i for i in range(cols)] for j in range(rows)]
		inner_zip = list(zip((image_array < 60),imrows,colrows))
		gdata = []
		for i in range(rows):
			l = list(filter(lambda x: x[0], list(zip(*inner_zip[i]))))
			if len(l) > 0:
				gdata.append(l)

		edges = []
		for vtcs in gdata:
			for vtx in vtcs:
				_, row, col = vtx
				if col - 1 > 0:
					edges.append(Edge(((row-1)*cols)+col-1, (row)*cols + col, image_array[row][col]))
				if col + 1 < cols:
					edges.append(Edge(((row-1)*cols)+col+1, (row)*cols + col, image_array[row][col]))
				edges.append(Edge(((row-1)*cols)+col, (row)*cols + col, image_array[row][col]))
		G = Graph(num_elems + 2, edges)
		if save_graph:
			G.to_csv(path/fname)
	return G


def get_components(G):
	rows = config.rows
	cols = config.cols
	uf = UF(G.V)
	for v in range(G.V):
		for e in G.adj[v]:
			uf.union(e._from(), e._to())
	components = defaultdict(list)
	for v in range(len(uf.roots)):
		components[uf.root(v)].append(v)

	temp_comp = dict()
	for k in components:
		lb, ub = min([c % cols for c in components[k]]), max([c % cols for c in components[k]])
		lbr, ubr = min([c // cols for c in components[k]]), max([c // cols for c in components[k]])
		if len(components[k]) > 5:
			temp_comp[k] = (lb, ub, lbr, ubr)
		
	return temp_comp
