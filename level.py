#!/usr/bin/python3

from gameobject import Ball, Palette #...
from vec2 import *
import sdl2

class Level:
	"""A single level representation."""

	def __init__(self, bricks):
		self.score = 0
		self.bonuses = []		
		self.palette = Palette()
		self.bricks  = bricks
		self.ball    = Ball(vec2(200, 400), vec2(0, 0), self.palette)

	def update(self):
		"""Update game state."""
		pass

	def collide(self, a, b):
		"""Checks if a and b collide with each other."""
		return NotImplemented

	def handleEvent(self, e):
		if e.type == sdl2.SDL_KEYDOWN:
			key = e.key.keysym.sym
			if key == sdl2.SDLK_LEFT:
				self.palette.move(-1)
			elif key == sdl2.SDLK_RIGHT:
				self.palette.move(+1)

	def render(self, renderer):
		self.palette.render(renderer)
		self.ball.render(renderer)
		for i in self.bricks:
			i.render(renderer)
		for j in self.bonuses:
			pass#j.render(renderer)