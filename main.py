#!/usr/bin/python3

import sys
import math
import sdl2.ext
from colour import Colour
from constants import *
from gameobject import Ball, Palette

from vec2 import vec2

BRICK_COLOUR = (0x22, 0x22, 0x99, 0xff)
INVUL_COLOUR = (0xf4, 0xbf, 0x42, 0xff)

RESOURCES = sdl2.ext.Resources(__file__, "resources")

level_data = [
	[0, 0, 1, 1, 0, 1, 1],
	[0, 1, 1, 2, 1, 2, 0],
	[1, 1, 2, 1, 2, 1, 1],
	[1, 1, 2, 1, 2, 1, 1]
]

#------------------------------

def brickToScreenCoords(pos):
	"""Turn brick's position into window pixel coordinates."""
	return pos.x * BRICKSIZE.x + SIDE_MARGIN, pos.y * BRICKSIZE.y + UPPER_MARGIN

# def physicalToScreenCoords(x, y):
	# """Turn physical coordinates into window pixel coordinates. Designed for objects such as ball or bonuses."""
	# return NotImplemented

def brickCoordsToRect(pos):
	"""Returns x-, y-position, width, height of a specific brick."""
	return brickToScreenCoords(pos) + tuple(BRICKSIZE)

#------------------------------

# Mainly-debug stuff.

def drawGrid(renderer, color=(0x44, 0x44, 0x44, 0xff)):
	"""Mainly for debugging purposes."""
	renderer.color = color
	for i in range(TILES.x):
		for j in range(0, TILES.y):
			renderer.draw_rect( brickCoordsToRect(vec2(i, j)) )

def dissectWindow(renderer):
	drawGrid(renderer)

	#renderer.draw_rect( (0, 0, SIDE_MARGIN, WINDOW_SIZE.y) )
	#renderer.draw_rect( (WINDOW_SIZE.x-SIDE_MARGIN, 0, SIDE_MARGIN, WINDOW_SIZE.y) )

	renderer.draw_rect( (0, 0, WINDOW_SIZE.x, UPPER_MARGIN) )
	renderer.draw_rect( (0, WINDOW_SIZE.y-LOWER_MARGIN, WINDOW_SIZE.x, LOWER_MARGIN) )

#------------------------------

def loadTextures(renderer):
	sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
	result = {}
	result["standard"] = sprite_factory.from_image(RESOURCES.get_path("brick.bmp"))
	result["invulnerable"] = sprite_factory.from_image(RESOURCES.get_path("invulnerable.bmp"))

	#result["palette"] = sprite_factory.from_image(RESOURCES.get_path("palette.bmp"))
	Palette.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("palette.bmp"))

	return result

def run():
	# Initialization.
	sdl2.ext.init()

	window = sdl2.ext.Window("pyNoid", size=tuple(WINDOW_SIZE), position=None, flags=sdl2.SDL_WINDOW_SHOWN)
	renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)

	spriterenderer = sdl2.ext.TextureSpriteRenderSystem(renderer)
	textures = loadTextures(renderer)

	palette = Palette()

	# Main loop.
	is_open = True
	while is_open:

		# Event loop.
		events = sdl2.ext.get_events()
		for e in events:
			if e.type == sdl2.SDL_QUIT:
				is_open = False
				break
			elif e.type == sdl2.SDL_KEYDOWN:
				key = e.key.keysym.sym
				if key == sdl2.SDLK_LEFT:
					pass
				elif key == sdl2.SDLK_RIGHT:
					pass
				elif key == sdl2.SDLK_ESCAPE:
					is_open = False
				break

		renderer.clear(color=(0, 0, 0, 0xff))		

		dissectWindow(renderer)

		for i,tab in enumerate(level_data):
			for j,_id in enumerate(tab):
				dest = brickCoordsToRect(vec2(j, i))
				if _id == 1:
					renderer.copy(textures["standard"], None, dest)
				elif _id == 2:
					renderer.copy(textures["invulnerable"], None, dest)					
		
		palette.render(renderer)
		renderer.present()

	sdl2.ext.quit()
	return 0


if __name__ == "__main__":
	sys.exit(run())