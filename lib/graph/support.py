class UF:

	def __init__(self, N):
		self.roots = [i for i in range(N)]
		self.num_elems = [1 for i in range(N)]


	def root(self, p):
		while self.roots[p] != p:
			self.roots[p] = self.roots[self.roots[p]]
			p = self.roots[p]
		return p


	def find(self, p, q):
		return self.roots[p] == self.roots[q]


	def union(self, p, q):
		i = self.root(p)
		j = self.root(q)

		if self.num_elems[i] < self.num_elems[j]:
			self.roots[i] = self.roots[j]
			self.num_elems[j] += self.num_elems[i]
		else:
			self.roots[j] = self.roots[i]
			self.num_elems[i] += self.num_elems[j]


class IndexMinPQ:

	def __init__(self, max_n):
		if max_n < 0:
			raise IllegalArgException()
		self.max_n = max_n
		self.N = 0
		self.keys = [None for i in range(max_n + 1)]
		self.pq = [None for i in range(max_n + 1)]
		self.qp = [-1 for i in range(max_n + 1)]

	def is_empty(self):
		return self.N == 0


	def contains(self, i):
		if i < 0 or i > self.max_n:
			raise IllegalArgException('illegal index')
		return self.qp[i] != -1


	def size(self):
		return self.N


	def insert(self, i, k):
		if i < 0 or i > self.max_n:
			raise IllegalArgException('illegal index')
		if self.contains(i):
			raise IllegalArgException('index is already in the priority queue')
			
		self.N += 1
		self.qp[i] = self.N
		self.pq[self.N] = i
		self.keys[i] = k
		self.swim(self.N)

	
	def min_index(self):
		if self.N == 0:
			raise NoSuchElementException("Priority queue underflow")
		return self.pq[1]


	def min_key(self):
		if self.N == 0:
			raise NoSuchElementException("Priority queue underflow")
		return self.keys[self.pq[1]]
	
	
	def del_min(self):
		if self.N == 0:
			raise NoSuchElementException("Priority queue underflow")
		pq_min = self.pq[1]
		self.exch(1, self.N)
		self.N -= 1
		self.sink(1)
		self.qp[pq_min] = -1
		self.keys[pq_min] = None
		self.pq[self.N + 1] = -1
		return pq_min


	def key_of(self, i):
		if i < 0 or i >= self.max_n:
			raise IllegalArgException('illegal index')
		if not self.contains(i):
			raise NoSuchElementException("index is not in the priority queue")
		return self.keys[i]


	def change_key(self, i, k):
		if i < 0 or i >= self.max_n:
			raise IllegalArgException('illegal index')
		if not self.contains(i):
			raise NoSuchElementException("index is not in the priority queue")
		self.keys[i] = k
		self.swim(self.qp[i])
		self.sink(self.qp[i])
	

	def decrease_key(self, i, k):
		if i < 0 or i >= self.max_n:
			raise IllegalArgException('illegal index')
		if not self.contains(i):
			raise NoSuchElementException("index is not in the priority queue")
		if self.keys[i] <= k:
			raise IllegalArgumentException("Calling decreaseKey() with given argument would not strictly decrease the key")
		self.keys[i] = k
		self.sink(self.qp[i])


	def delete(self, i):
		if i < 0 or i >= self.max_n:
			raise IllegalArgException('illegal index')
		if not self.contains(i):
			raise NoSuchElementException("index is not in the priority queue")
		ind = self.qp[i]
		self.exch(ind, self.N)
		self.N -= 1
		self.swim(ind)
		self.sink(ind)
		self.keys[i] = None
		self.qp[i] = -1

	
	def swim(self, k):
		while (k > 1) and (self.greater(k//2, k)):
			self.exch(k, k//2)
			k //= 2

	def sink(self, k):
		while (2*k <= self.N):
			j = 2*k
			if (j < self.N) and (self.greater(j, j+1)): 
				j += 1
			if not self.greater(k, j):
				break
			self.exch(k, j)
			k = j

	def greater(self, i, j):
		# for more general comparable data types, implement as follows:
		# return self.keys[self.pq[i]].compare_to(self.keys[self.pq[j]]) > 0
		# for now, only expecting floats
		return self.keys[self.pq[i]] > self.keys[self.pq[j]]

	def exch(self, i, j):
		temp = self.pq[i]
		self.pq[i] = self.pq[j]
		self.pq[j] = temp
		self.qp[self.pq[i]] = i
		self.qp[self.pq[j]] = j



class Queue:
	
	def __init__(self):
		self.q = []
		self.q_len = 0
		self.i = 0

	def enqueue(self, i):
		self.q.append(i)
		self.q_len += 1
		self.i += 1


	def dequeue(self):
		i = self.q[0]
		self.q = self.q[1:]
		self.q_len -= 1
		self.i -= 1
		return i


	def is_empty(self):
		return self.q_len == 0


	def size(self):
		return self.q_len


	def __repr__(self):
		rep_str = '\n'.join([str(elem) for elem in self.q])
		return rep_str


	def __next__(self):
		if self.i > 0:
			i = self.i
			self.i -= 1
			return self.q[self.q_len - i]
		self.i = self.q_len
		raise StopIteration()


	def __iter__(self):
		return self


class MinPQ:

	def __init__(self):
		self.pq = [None]
		self.N = 0


	def is_empty():
		return self.N == 0


	def insert(self, k):
		self.pq.append(k)
		self.N += 1
		self.swim(self.N)

	
	def del_min():
		pq_min = self.pq[1]
		self.exch(1, self.N)
		self.N -= 1
		self.sink(1)
		self.pq[N + 1] = None
		return pq_min


	def swim(self, k):
		while (k > 1) and (self.greater(k//2, k)):
			self.exch(k, k//2)
			k //= 2


	def sink(self, k):
		while (2*k <= self.N):
			j = 2*k
			if (j < self.N) and (self.greater(j, j+1)): 
				j += 1
			if not self.greater(k, j):
				break
			self.exch(k, j)
			k = j


	def greater(i, j):
		#return self.pq[i].compare_to(self.pq[j])
		return self.pq[i] > self.pq[j]


	def exch(self, i, j):
		temp = self.pq[i]
		self.pq[i] = self.pq[j]
		self.pq[j] = temp


class Stack:
	
	def __init__(self):
		self.stack = []
		self.size = 0
		

	def push(self, i):
		self.stack.append(i)
		self.size += 1


	def pop(self):
		i = self.stack[-1]
		self.stack = self.stack[:-1]
		self.size -= 1
		return i


	def is_empty(self):
		return self.size  == 0


	def size(self):
		return self.size
