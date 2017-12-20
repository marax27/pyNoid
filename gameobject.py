#!/usr/bin/python3

import dev
import math
import collision
from vec2 import *
from constants import *

import sdl2

#------------------------------------------------------------

# def brickToScreenCoords(x, y):
# 	"""Turn brick's position into window pixel coordinates."""
# 	return x * BRICKSIZE.x + SIDE_MARGIN, y * BRICKSIZE.y + UPPER_MARGIN

# def brickCoordsToRect(x, y):
# 	"""Returns x-, y-position, width, height of a specific brick."""
# 	return brickToScreenCoords(x, y) + tuple(BRICKSIZE)

#------------------------------------------------------------

class Wall:
	TEXTURE = None

class GameObject:
	"""GameObject - base class for many game objects (duh)."""
	def __init__(self, position):
		self.position = position

class Brick(GameObject):
	"""A brick class."""
	TEXTURES = None
	EMPTY, REGULAR, HEAVY, HEAVIER, INVULNERABLE = range(5)
	
	def __init__(self, position, brick_type):
		super().__init__(position)
		self.brick_type = brick_type

	def handleCollision(self):
		"""React to ball collision."""
		if self.brick_type == Brick.REGULAR:
			self.brick_type = Brick.EMPTY
		elif self.brick_type == Brick.HEAVY:
			self.brick_type = Brick.REGULAR
		elif self.brick_type == Brick.HEAVIER:
			self.brick_type = Brick.HEAVY
		else:
			pass

	def screenPos(self):
		return self.position.x * BRICKSIZE.x + SIDE_MARGIN, self.position.y * BRICKSIZE.y + UPPER_MARGIN
	
	def rect(self):
		return self.screenPos() + tuple(BRICKSIZE)

	def render(self, renderer):
		bt = self.brick_type
		if bt != self.EMPTY:
			renderer.copy(self.TEXTURES[self.brick_type], None, self.rect())


class PhysicalObject(GameObject):
	"""PhysicalObject - base class for bonuses and balls."""
	def __init__(self, position, velocity):
		super().__init__(position)
		self.velocity = velocity
	
class Palette(GameObject):
	"""Palette representation."""
	TEXTURE = None
	SIZE = vec2(140, 20)
	SPEED = 20

	def __init__(self):
		super().__init__(vec2(
			self.SIZE.x // 2,
			WINDOW_SIZE.y - self.SIZE.y - 10
		))

	def move(self, offset):
		new_x = self.position.x + offset * self.SPEED
		self.setPosition(new_x)
	
	def setPosition(self, x):
		if x == self.position.x: return;
		if x < 0:
			x = 0
		elif x >= WINDOW_SIZE.x - self.SIZE.x:
			x = WINDOW_SIZE.x - self.SIZE.x
		self.position.x = x
		dev.report('pmov', self.position.x)

	def render(self, renderer):
		if self.TEXTURE is not None:
			renderer.copy(self.TEXTURE, None, vectorsToTuple(self.position, self.SIZE))

	def rect(self):
		return tuple(self.position) + tuple(self.SIZE)

class Ball(PhysicalObject):
	"""Ball class"""
	TEXTURE = None
	RADIUS = 7
	SPEED = 6.0

	def __init__(self, position, velocity, binding=None):
		super().__init__(position, self.SPEED*velocity.normalized()) 
		self.binding = binding  # If a ball lies upon a palette, binding represents
		                        # the palette. If ball flies, binding=None.

	def handleCollision(self, collision_type):
		v = self.velocity.clone()
		if collision_type in (collision.NO_COLLISION, collision.INSIDE):
			return
		elif collision_type == collision.X_AXIS_COLLISION:
			self.velocity.x = -self.velocity.x
		elif collision_type == collision.Y_AXIS_COLLISION:
			self.velocity.y = -self.velocity.y
		elif collision_type == collision.CORNER_NEG_COLLISION:
			self.velocity.x, self.velocity.y = -self.velocity.y, -self.velocity.x
		elif collision_type == collision.CORNER_COLLISION:
			self.velocity.x, self.velocity.y = self.velocity.y, self.velocity.x			
		dev.report('wbcoll', collision_type, v, self.velocity)

	def handlePaletteCollision(self, collision_type, palette):
		if collision_type != collision.NO_COLLISION:
			v = self.velocity.clone()
			a = self.position.x + self.RADIUS - palette.position.x
			w = palette.SIZE.x
			eta_prim = -math.pi/3.0 * math.cos(a * math.pi / w)
			self.velocity = vec2(
				math.sin(eta_prim),
				-math.cos(eta_prim)
			)
			dev.report('pcoll', collision_type, v, self.velocity)

	def render(self, renderer):
		p = self.position
		t = int(p.x), int(p.y), 2*self.RADIUS, 2*self.RADIUS
		renderer.copy(self.TEXTURE, None, t )

	def update(self):
		self.position += self.velocity.normalized() * self.SPEED * DELTA_T