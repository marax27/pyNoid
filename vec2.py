#!/usr/bin/python3

import math

class vec2(object):
	"""The 2D vector class."""

	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def clone(self):
		return vec2(self.x, self.y)
	
	def length(self):
		"""Returns length (norm, magnitude) of the vector."""
		return math.sqrt(self.x*self.x + self.y*self.y)

	def normalized(self):
		"""Returns a normalized unit vector."""
		length = self.length()
		if length == 0.0:
			return self
		return vec2(self.x / length, self.y / length)

	def __getitem__(self, key):
		"""Alternative way of calling out elements."""
		if key == 0:    return self.x;
		elif key == 1:  return self.y;
		else:  raise IndexError("Invalid element number: only 0 or 1 allowed.")

	def __repr__(self):
		return "[%f, %f]" % (self.x, self.y)

	# Operator overloading.
	def __add__(self, right):
		return vec2(self.x + right.x, self.y + right.y)

	def __sub__(self, right):
		return vec2(self.x - right.x, self.y - right.y)

	def __mul__(self, scalar):
		"""Returns vector multiplied by a scalar."""
		return vec2(self.x * scalar, self.y * scalar)

	def __rmul__(self, scalar):
		"""__mul__ equivalent when expression looks like 'scalar * vector'"""
		return self.__mul__(scalar)

	def __truediv__(self, scalar):
		"""Vector division."""
		return vec2(self.x / scalar, self.y / scalar)

	def __div__(self, scalar):
		"""Vector integer division."""
		return vec2(self.x // scalar, self.y // scalar)

	def __neg__(self):
		"""Equivalent of -1 * vector"""
		return vec2(-self.x, -self.y)

# Other functions.
def vectorsToTuple(v1, v2):
	return tuple(v1) + tuple(v2)

def intmatch(v1, v2):
	return int(v1.x) == int(v2.x) and int(v1.y) == int(v2.y)