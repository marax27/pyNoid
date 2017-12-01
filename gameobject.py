#!/usr/bin/python3

from vec2 import *
from constants import WINDOW_SIZE

class GameObject:
	"""GameObject - base class for many game objects (duh)."""
	def __init__(self, position):
		self.position = position

class PhysicalObject(GameObject):
	"""PhysicalObject - base class for bonuses and balls."""
	def __init__(self, position, velocity):
		super().__init__(position)
		self.velocity = velocity

class Palette(GameObject):
	"""Palette representation."""
	TEXTURE = None
	SIZE = vec2(200, 30)
	SPEED = 20

	def __init__(self):
		super().__init__(vec2(
			self.SIZE.x // 2,
			WINDOW_SIZE.y - self.SIZE.y - 10
		))

	def move(self, offset):
		new_x = self.position.x + offset * self.SPEED
		if new_x < 0:
			new_x = 0
		elif new_x >= WINDOW_SIZE.x - self.SIZE.x:
			new_x = WINDOW_SIZE.x - self.SIZE.x
		self.position.x = new_x
	
	def render(self, renderer):
		if self.TEXTURE is not None:
			renderer.copy(self.TEXTURE, None, vectorsToTuple(self.position, self.SIZE))

class Ball:
	"""Ball class"""
	RADIUS = 15
	SPEED = 3.0

	def __init__(self, x, y, binding=None):
		self.x = x
		self.y = y
		self.velocity = 0.0, 0.0
		self.binding = binding  # If a ball lies upon a palette, binding represents
		                        # the palette. If ball flies, binding=None.
		self.attached = None

	def render(self, renderer):
		_x, _y = int(self.x), int(self.y)
		renderer.draw_line((_x - self.RADIUS, _y, _x + self.RADIUS, _y), (0xff, 0xff, 0xff, 0xff))
		renderer.draw_line((_x, _y - self.RADIUS, _x, _y + self.RADIUS), (0xff, 0xff, 0xff, 0xff))

	def update(self, dt):
		if self.attached is None:
			self.x += dt * 5
			self.y += dt * 5
		else:
			pass