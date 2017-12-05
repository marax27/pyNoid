#!/usr/bin/python3

from gameobject import Ball, Palette #...
import constants
from vec2 import *
import sdl2

class Level:
	"""A single level representation."""

	def __init__(self, bricks):
		self.score = 0
		self.bonuses = []		
		self.palette = Palette()
		self.bricks  = bricks
		self.ball    = Ball(vec2(200, 400), vec2(3, 2), self.palette)

	def update(self):
		"""Update game state."""
		# 1. Update objects' positions.
		self.ball.update()
		for i in self.bonuses:
			pass  #i.update()
		
		# 2. Check for collisions.
		#          WALLS BALL PALETTE BONUSES BRICKS
		#   WALLS    0    1     1       1       0
		#    BALL    1    0     1       0       1
		# PALETTE    1    1     0       1       0
		# BONUSES    1    0     1       0       0
		#  BRICKS    0    1     0       0       0
		#
		# a)ball-wall        circle-box
		# b)ball-palette     circle-box
		# c)ball-bricks      circle-box
		# d)wall-palette     box-box
		# e)wall-bonuses     box-box
		# f)bonuses-palette  box-box
	
		# 2a)
		bpos, r = self.ball.position, self.ball.RADIUS
		gs = constants.gameSpace()
		if (bpos.x <= gs[0]) or (bpos.x + 2*r >= gs[0] + gs[2]):
			self.ball.velocity.x = -self.ball.velocity.x
		elif (bpos.y <= gs[1]) or (bpos.y + 2*r >= gs[1] + gs[3]):
			self.ball.velocity.y = - self.ball.velocity.y

		# 2b)

	def collide(self, a, b):
		"""Checks if a and b collide with each other."""
		return NotImplemented

	def handleEvent(self, e):
		"""Process events such as palette movement."""
		if e.type == sdl2.SDL_KEYDOWN:
			key = e.key.keysym.sym
			if key == sdl2.SDLK_LEFT:
				self.palette.move(-1)
			elif key == sdl2.SDLK_RIGHT:
				self.palette.move(+1)

	def render(self, renderer):
		"""Render the level."""
		self.palette.render(renderer)
		self.ball.render(renderer)
		for i in self.bricks:
			i.render(renderer)
		for j in self.bonuses:
			pass#j.render(renderer)