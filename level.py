#!/usr/bin/python3

from gameobject import Ball, Palette, Brick
from collision import *
from vec2 import *
import constants
import sdl2

class Level:
	"""A single level representation."""

	def __init__(self, bricks):
		self.endgame = False
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
	
		bpos = self.ball.position
		r = self.ball.RADIUS

		# 2a)
		gs = constants.gameSpace()
		self.ball.handleCollision(circleLineCollision(bpos, r, x=gs[0]))
		self.ball.handleCollision(circleLineCollision(bpos, r, y=gs[1]))
		self.ball.handleCollision(circleLineCollision(bpos, r, x=gs[0]+gs[2]))
		if(circleLineCollision(bpos, r, y=gs[1]+gs[3]) != NO_COLLISION):
			self.endgame = True
			return

		# 2b)
		c = circleBoxCollision(bpos, r, self.palette.rect())
		self.ball.handlePaletteCollision(c, self.palette)
		
		# 2c)
		hits = 0
		to_delete = []
		for i in self.bricks:
			c = circleBoxCollision(bpos, r, i.rect())
			if c != NO_COLLISION:
				hits += 1
				self.ball.handleCollision(c)

				i.handleCollision()
				if i.brick_type == Brick.EMPTY:
					to_delete.append(i)
				
				if hits >= 2:
					break
		self.bricks = [x for x in self.bricks if x not in to_delete]

	def handleEvent(self, e):
		"""Process events such as palette movement."""
		if e.type == sdl2.SDL_MOUSEMOTION:
			x = e.motion.x
			self.palette.setPosition(x)
			
			# Since palette is considered unstoppable force, if palette now
			# covers space occupied by the ball, the ball must bend.
			c = circleBoxCollision(self.ball.position, self.ball.RADIUS, self.palette.rect())
			if c != NO_COLLISION:
				self.ball.position.y = self.palette.position.y - 2*self.ball.RADIUS

		# Deprecated: moving palette with a keyboard.
		"""if e.type == sdl2.SDL_KEYDOWN:
			key = e.key.keysym.sym
			if key == sdl2.SDLK_LEFT:
				self.palette.move(-1)
			elif key == sdl2.SDLK_RIGHT:
				self.palette.move(+1)"""

	def render(self, renderer):
		"""Render the level."""
		self.palette.render(renderer)
		if not self.endgame:
			self.ball.render(renderer)
		for i in self.bricks:
			i.render(renderer)
		for j in self.bonuses:
			pass#j.render(renderer)