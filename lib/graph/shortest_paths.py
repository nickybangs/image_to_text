import numpy as np

from edge_weighted_digraph import *
from support import *


class DijsktraSP:
	'''Dijsktra's SP algorithm'''

	def __init__(self, G, s):
		self.edge_to = [None for i in range(G.V)]
		self.dist_to = [np.inf for i in range(G.V)]
		self.pq = IndexMinPQ(G.V)
		
		self.dist_to[s] = 0.0
		self.pq.insert(s, 0.0)
		while not self.pq.is_empty():
			v = self.pq.del_min()
			for e in G.adj[v]:
				self.relax(e)

	
	def relax(self, e):
		v = e._from()
		w = e._to()
		if self.dist_to[w] > self.dist_to[v] + e.weight:
			self.dist_to[w] = self.dist_to[v] + e.weight
			self.edge_to[w] = e
			if self.pq.contains(w):
				self.pq.decrease_key(w, self.dist_to[w])
			else:
				self.pq.insert(w, self.dist_to[w])
