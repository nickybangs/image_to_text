from collections import defaultdict
import numpy as np
from directed_edge import *

class EdgeWeightedDigraph:

	def __init__(self, V, edges):
		self.V = int(V)
		self.adj = [[] for i in range(self.V)]
		self.E = 0
		for edge in edges:
			self.add_edge(edge)


	@classmethod
	def from_filename(cls, f):
		with open(f, 'r') as graph_file:
			V = int(graph_file.readline())
			edges = []
			for edge in graph_file.readlines():
				vs, weight = edge.strip().split(' ')
				v, w = map(int, vs.split('-'))
				edges.append(DirectedEdge(v, w, float(weight)))
		return cls(V, edges)


	def to_csv(self, f):
		with open(f, 'w') as graph_file:
			graph_file.write('{}\n'.format(self.V))
			for v in range(self.V):
				for e in self.adj[v]:
					graph_file.write('{}-{} {}\n'.format(e._from(), e._to(), e.weight))


	def add_edge(self, e):
		v = int(e._from())
		self.adj[v].append(e)
		self.E += 1

	def __repr__(self):
		graph_string = ''
		for i in range(self.V):
			for other in self.adj[i]:
				graph_string += '{}\n'.format(other)
		return graph_string
