#!/usr/bin/python3

from gameobject import Ball, Palette, Brick, Wall
from collision import *
from vec2 import *
import gameinstance
import constants
import misc
import sdl2
import hud

class Level(gameinstance.GameInstance):
	"""A single level representation."""

	class Score:
		BRICK_HIT = 10
		# TODO

	def __init__(self, bricks):
		self.endgame = False
		self.score = 0
		self.lives = 3
		self.bonuses = []		
		self.palette = Palette()
		self.bricks  = bricks
		self.ball    = Ball(vec2(0, 0), vec2(0, 1), self.palette)

		mx, my = misc.getMousePos()
		self.palette.setPosition(mx)

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
		MAGIC = 14  #lowers the 'death zone', so that the game doesn't stop
		            #immediately as ball hits the bottom of the window. 
		gs = constants.gameSpace()
		self.ball.handleCollision(circleLineCollision(bpos, r, x=gs[0]))
		self.ball.handleCollision(circleLineCollision(bpos, r, y=gs[1]))
		self.ball.handleCollision(circleLineCollision(bpos, r, x=gs[0]+gs[2]))
		if(circleLineCollision(bpos, r, y=gs[1]+gs[3]+MAGIC) != NO_COLLISION):
			self.lives -= 1
			if self.lives == 0:
				self.endgame = True
			else:
				self.restart()
			#return

		# 2b)
		c = circleBoxCollision(bpos, r, self.palette.rect())
		self.ball.handlePaletteCollision(c, self.palette)
		
		# 2c)
		hit_bricks, to_delete = [], []
		for i in self.bricks:
			c = circleBoxCollision(bpos, r, i.rect())
			if c == NO_COLLISION:
				continue

			hit_bricks.append( (i, c) )
			i.handleCollision()
			if i.brick_type == Brick.EMPTY:
				to_delete.append(i)
			
			if len(hit_bricks) > 1:
				break
		
		if len(hit_bricks) < 2:
			for i in hit_bricks:
				self.ball.handleCollision(i[1])
		elif int(hit_bricks[0][0].position.y) == int(hit_bricks[1][0].position.y):
			self.ball.handleCollision(Y_AXIS_COLLISION)
		elif int(hit_bricks[0][0].position.x) == int(hit_bricks[1][0].position.x):
			self.ball.handleCollision(X_AXIS_COLLISION)
		else:
			self.ball.handleCollision(CORNER_NEG_COLLISION)

		for i, j in hit_bricks:
			if i.brick_type != Brick.INVULNERABLE:
				self.score += self.Score.BRICK_HIT

		# hits = 0
		# to_delete = []
		# for i in self.bricks:
			# c = circleBoxCollision(bpos, r, i.rect())
			# if c != NO_COLLISION:
				# hits += 1
				# self.ball.handleCollision(c)

				# i.handleCollision()
				# if i.brick_type == Brick.EMPTY:
					# to_delete.append(i)
				# 
				# if hits > 1:
					# break
		self.bricks = [x for x in self.bricks if x not in to_delete]

		# 2d)
		p_x = self.palette.position.x
		if p_x < gs[0]:
			self.palette.position.x = gs[0]
		elif p_x + self.palette.SIZE.x > gs[0] + gs[2]:
			self.palette.position.x = gs[0] + gs[2] - self.palette.SIZE.x

	def handleEvent(self, e):
		"""Process events such as palette movement."""
		
		if e.type == sdl2.SDL_MOUSEMOTION:
			# Since palette is considered unstoppable force, if palette now
			# covers space occupied by the ball, the ball must bend.

			x = e.motion.x
			self.palette.setPosition(x)

			c = circleBoxCollision(self.ball.position, self.ball.RADIUS, self.palette.rect())
			if c != NO_COLLISION:
				#self.ball.position.y = self.palette.position.y - 2*self.ball.RADIUS
				r = self.ball.RADIUS
				bx, px = self.ball.position.x + r, self.palette.position.x
				gs = constants.gameSpace()
				if bx < px + r and px > gs[0] + 2*r:
					# Shift left.
					self.ball.position.x = px - 2*r
				elif bx>px + self.palette.SIZE.x-r and px+self.palette.SIZE.x < gs[0]+gs[2]-2*r:
					# Shift right.
					self.ball.position.x = px + self.palette.SIZE.x
				else:
					# Shift up.
					self.ball.position.y = self.palette.position.y - 2*r

		elif e.type == sdl2.SDL_MOUSEBUTTONDOWN:
			if e.button.button == sdl2.SDL_BUTTON_LEFT:
				self.ball.handleMouseKey()

		# Deprecated: moving palette with a keyboard.
		"""if e.type == sdl2.SDL_KEYDOWN:
			key = e.key.keysym.sym
			if key == sdl2.SDLK_LEFT:
				self.palette.move(-1)
			elif key == sdl2.SDLK_RIGHT:
				self.palette.move(+1)"""

	def render(self, renderer):
		"""Render the level."""
		
		renderer.copy(Wall.TEXTURE, None, (0, 0, constants.SIDE_MARGIN, constants.WINDOW_SIZE.y))
		renderer.copy(Wall.TEXTURE, None, (constants.WINDOW_SIZE.x-constants.SIDE_MARGIN, 0, constants.SIDE_MARGIN, constants.WINDOW_SIZE.y))

		self.palette.render(renderer)
		if not self.endgame:
			self.ball.render(renderer)
		for i in self.bricks:
			i.render(renderer)
		for j in self.bonuses:
			pass#j.render(renderer)

		h = hud.Text(str(self.score), renderer, size=constants.UPPER_MARGIN-10)
		h.render(renderer, (constants.SIDE_MARGIN + 50, 5))

		h.load(str(self.lives), renderer, size=constants.UPPER_MARGIN-10)
		h.render(renderer, (constants.WINDOW_SIZE.x - constants.SIDE_MARGIN - 80, 5))

	def restart(self):
		self.ball = Ball(vec2(0, 0), vec2(0, 1), self.palette)

	def isOpen(self):
		"""Returns False if GameInstance should be no longer active."""
		return not self.endgame