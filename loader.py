#!/usr/bin/python3

from gameobject import Brick, Palette, Ball
from vec2 import vec2
import sdl2.ext

RESOURCES = sdl2.ext.Resources(__file__, "resources")

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

def loadTextures(renderer):
	"""Load necessary textures from drive."""
	sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

	Palette.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("palette.bmp"))
	Ball.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("ball.png"))
	Brick.TEXTURES = {
		Brick.REGULAR : sprite_factory.from_image(RESOURCES.get_path("brick.bmp")),
		Brick.INVULNERABLE : sprite_factory.from_image(RESOURCES.get_path("invulnerable.bmp"))
	}