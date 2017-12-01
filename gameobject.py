#!/usr/bin/python3

"""Palette class"""
class Palette:
	HEIGHT = 30
	COLOR = (0x77, 0x77, 0x77, 0xff)
	SPEED = 20

	def __init__(self):
		self.x = int(WINDOW_SIZE[0] * 0.25)
		self.y = WINDOW_SIZE[1] - self.HEIGHT - 10
		self.width = 200
	
	def rect(self):
		return self.x, self.y, self.width, self.HEIGHT

	def move(self, direction):
		new_x = self.x + direction * self.SPEED
		if new_x < 0:
			new_x = 0
		elif new_x >= WINDOW_SIZE[0] - self.width:
			new_x = WINDOW_SIZE[0] - self.width
		self.x = new_x

"""Ball class"""
class Ball:
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