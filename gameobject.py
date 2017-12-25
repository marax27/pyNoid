#!/usr/bin/python3

import dev
import copy
import math
import random
import collision
from vec2 import *
from constants import *
from misc import randomWithWeights
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

#-----------------------------------------------------------

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

	def center(self):
		sp = self.screenPos()
		return vec2(sp[0] + BRICKSIZE.x//2, sp[1] + BRICKSIZE.y//2)

#-----------------------------------------------------------

class PhysicalObject(GameObject):
	"""PhysicalObject - base class for bonuses and balls."""
	def __init__(self, position, velocity):
		super().__init__(position)
		self.velocity = velocity

#-----------------------------------------------------------

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
		if x == self.position.x:
			return
		if x < SIDE_MARGIN:
			x = SIDE_MARGIN
		elif x >= WINDOW_SIZE.x - self.SIZE.x - SIDE_MARGIN:
			x = WINDOW_SIZE.x - self.SIZE.x - SIDE_MARGIN
		self.position.x = x
		dev.report('pmov', self.position.x)

	def render(self, renderer):
		if self.TEXTURE is not None:
			renderer.copy(self.TEXTURE, None, vectorsToTuple(self.position, self.SIZE))

	def rect(self):
		return tuple(self.position) + tuple(self.SIZE)

#-----------------------------------------------------------

class Ball(PhysicalObject):
	"""Ball class"""
	TEXTURE = None
	RADIUS = 7
	SPEED = 6.0

	def __init__(self, position, velocity, binding=None):
		super().__init__(position, self.SPEED*velocity.normalized()) 
		self.binding = binding  # If a ball lies upon a palette, binding represents
		                        # the palette. If ball flies, binding=None.
		if binding:
			position = binding.position + vec2(20, -2*self.RADIUS)

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

	def handleMouseKey(self):
		if self.binding:
			pal = copy.copy(self.binding)
			self.binding = None
			self.handlePaletteCollision(collision.Y_AXIS_COLLISION, pal)

	def handlePaletteCollision(self, collision_type, palette):
		if self.binding or collision_type == collision.NO_COLLISION:
			return

		if collision_type == collision.Y_AXIS_COLLISION:
			v = self.velocity.clone()
			a = self.position.x + self.RADIUS - palette.position.x
			w = palette.SIZE.x
			eta_prim = -math.pi/3.0 * math.cos(a * math.pi / w)
			self.velocity = vec2(
				math.sin(eta_prim),
				-math.cos(eta_prim)
			)
			dev.report('pcoll', collision_type, v, self.velocity)
		elif collision_type == collision.X_AXIS_COLLISION:
			self.handleCollision(collision.X_AXIS_COLLISION)

	def render(self, renderer):
		p = self.position
		t = int(p.x), int(p.y), 2*self.RADIUS, 2*self.RADIUS
		renderer.copy(self.TEXTURE, None, t)

	def update(self):
		if not self.binding:
			self.position += self.velocity.normalized() * self.SPEED * DELTA_T
		else:
			self.position = self.binding.position + vec2(20, -2*self.RADIUS)

#-----------------------------------------------------------

class Type:
	def __init__(self, weight, rect):
		self.weight = weight
		self.rect = rect

class Bonus(PhysicalObject):
	"""Base class for all bonuses/pickups."""
	TEXTURE = None
	START_SPEED = 7.0

	# Types of bonuses.
	EXTRA_LIFE       = 0x2001
	TECH_SUPPORT     = 0x2002
	WIDER_PALETTE    = 0x2003
	NARROWER_PALETTE = 0x2004
	SUPER_SPEED	     = 0x2005
	STRIKE_THROUGH   = 0x2006
	FIREBALL         = 0x2007
	DEATH            = 0x2008
	SKYFALL          = 0x2009
	CATCH_N_HOLD     = 0x200a
	# ... TODO


	"""Dictionary of possible bonuses' types. Type code is a key, whereas a value is the weight."""
	types = {
		EXTRA_LIFE       : Type(6,  (0, 0, BONUS_SIZE, BONUS_SIZE)),
		TECH_SUPPORT     : Type(12, (BONUS_SIZE, 0, BONUS_SIZE, BONUS_SIZE)),
		WIDER_PALETTE    : Type(36, (2*BONUS_SIZE, 0, BONUS_SIZE, BONUS_SIZE)),
		NARROWER_PALETTE : Type(36, (3*BONUS_SIZE, 0, BONUS_SIZE, BONUS_SIZE)),
		SUPER_SPEED      : Type(20, (4*BONUS_SIZE, 0, BONUS_SIZE, BONUS_SIZE)),
		STRIKE_THROUGH   : Type(12, (0, BONUS_SIZE, BONUS_SIZE, BONUS_SIZE)),
		FIREBALL         : Type(12, (BONUS_SIZE, BONUS_SIZE, BONUS_SIZE, BONUS_SIZE)),
		DEATH            : Type(20, (2*BONUS_SIZE, BONUS_SIZE, BONUS_SIZE, BONUS_SIZE)),
		SKYFALL          : Type(8,  (3*BONUS_SIZE, BONUS_SIZE, BONUS_SIZE, BONUS_SIZE)),
		CATCH_N_HOLD     : Type(8,  (4*BONUS_SIZE, BONUS_SIZE, BONUS_SIZE, BONUS_SIZE))
	}

	def __init__(self, position, bonus_type=None):
		"""Create new bonus. Initial velocity angle is randomly generated."""
		self.position = position - vec2(BONUS_SIZE//2, BONUS_SIZE//2)

		# Randomly select the bonus type.
		if not bonus_type:
			#bonus_type = randomDict(self.types)
			bonus_type = randomWithWeights(list(self.types.keys()), [x.weight for x in self.types.values()])

		self.type = bonus_type

		phi = random.random() * math.pi
		self.velocity = self.START_SPEED * vec2(math.cos(phi), -math.sin(phi))
	
	def update(self):
		self.position += vec2(
			self.velocity.x * DELTA_T,
			self.velocity.y * DELTA_T + G_ACCEL * DELTA_T * DELTA_T
		)
		self.velocity.y += G_ACCEL * DELTA_T
	
	def handleCollision(self, collision_type):
		if collision_type == collision.X_AXIS_COLLISION:
			self.velocity.x = -self.velocity.x
		elif collision_type == collision.Y_AXIS_COLLISION:
			self.velocity.y = -self.velocity.y
	
	def render(self, renderer):
		# TODO
		t = int(self.position.x), int(self.position.y), BONUS_SIZE, BONUS_SIZE
		renderer.copy(self.TEXTURE, self.types[self.type].rect, t)

	def rect(self):
		return tuple(self.position) + (BONUS_SIZE, BONUS_SIZE)

