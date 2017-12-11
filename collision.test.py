#!/usr/bin/python3

import unittest
from math import sqrt
from vec2 import vec2
from collision import *

class TestCollision(unittest.TestCase):

	def test_circleBoxCollision(self):
		self.assertTrue(circleBoxCollisionNew(vec2(0,0), 5, (5, 5, 0, 0)))
		self.assertTrue(circleBoxCollisionNew(vec2(-5,-5), 5, (0, 0, 0, 0)))
		self.assertTrue(circleBoxCollisionNew(vec2(-5,0), 5, (0, 0, 0, 0)))
		self.assertTrue(circleBoxCollisionNew(vec2(0,5), 5, (0, 0, 0, 0)))

if __name__ == "__main__":
	unittest.main()