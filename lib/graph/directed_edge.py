
class DirectedEdge:

	def __init__(self, v, w, weight):
		self.v = v
		self.w = w
		self.weight = weight


	def _from(self):
		return self.v


	def _to(self):
		return self.w


	def __repr__(self):
		return '{} -> {}, {}'.format(self.v, self.w, self.weight)
