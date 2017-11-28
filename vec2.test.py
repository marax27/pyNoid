#!/usr/bin/python3

import unittest
from math import sqrt
from vec2 import vec2

a, b, c, d = 3.45, 9.39, 7.30, 6.66

class TestVec2(unittest.TestCase):

	def test_length(self):
		self.assertAlmostEqual(vec2(a, b).length(), sqrt(a*a + b*b))
		self.assertEqual(vec2(0, 0).length(), 0)
	
	def test_normalized(self):
		self.assertAlmostEqual(vec2(a, b).normalized().length(), 1.0)
	
	def test_getitem(self):
		v = vec2(a, b)
		self.assertTrue(v[0] is v.x)
		self.assertTrue(v[1] is v.y)

	#def test_repr()

	def test_add(self):
		v, w = vec2(a, b), vec2(c, d)
		self.assertAlmostEqual((v+w).x, v.x+w.x)
		self.assertAlmostEqual((v+w).y, v.y+w.y)

	def test_sub(self):
		v, w = vec2(a, b), vec2(c, d)
		self.assertAlmostEqual((v-w).x, v.x-w.x)
		self.assertAlmostEqual((v-w).y, v.y-w.y)

	def test_mul(self):
		v = vec2(a, b)
		self.assertAlmostEqual((v*a).x, a*v.x)
		self.assertAlmostEqual((v*a).y, a*v.y)
	
	def test_rmul(self):
		v = vec2(a, b)
		self.assertAlmostEqual((a*v).x, a*v.x)
		self.assertAlmostEqual((a*v).y, a*v.y)
	
	def test_truediv(self):
		v = vec2(a, b)
		self.assertAlmostEqual((v/a).x, v.x/a)
		self.assertAlmostEqual((v/a).y, v.y/a)
	
	def test_neg(self):
		self.assertAlmostEqual(-vec2(a, b).x, vec2(-a, -b).x)
		self.assertAlmostEqual((-vec2(a, b)).y, vec2(-a, -b).y)

if __name__ == "__main__":
	unittest.main()