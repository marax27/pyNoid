#!/usr/bin/python3

from gameobject import Brick
from vec2 import vec2

def loadLevel(a):
	"""Returns array of bricks that makes a level."""
	return [
		Brick(vec2(1, 1), Brick.INVULNERABLE),
		Brick(vec2(2, 1), Brick.INVULNERABLE),
		Brick(vec2(1, 2), Brick.INVULNERABLE),
		Brick(vec2(2, 2), Brick.REGULAR),		
		Brick(vec2(3, 2), Brick.REGULAR),		
		Brick(vec2(2, 3), Brick.REGULAR)		
	]