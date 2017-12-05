#!/usr/bin/python3

import sys
import math
import sdl2.ext
import level
import loader
from colour import Colour
from constants import *
from gameobject import Ball, Palette, Brick

from vec2 import vec2

BRICK_COLOUR = (0x22, 0x22, 0x99, 0xff)
INVUL_COLOUR = (0xf4, 0xbf, 0x42, 0xff)

RESOURCES = sdl2.ext.Resources(__file__, "resources")

# Mainly-debug stuff.
def drawGrid(renderer, color=(0x44, 0x44, 0x44, 0xff)):
	"""Mainly for debugging purposes."""
	renderer.color = color
	for i in range(TILES.x):
		for j in range(0, TILES.y):
			pass

def dissectWindow(renderer):
	drawGrid(renderer)

	renderer.draw_rect( (0, BRICKSIZE.y*2, SIDE_MARGIN, WINDOW_SIZE.y-BRICKSIZE.y*2) )
	renderer.draw_rect( (WINDOW_SIZE.x-SIDE_MARGIN, BRICKSIZE.y*2, SIDE_MARGIN, WINDOW_SIZE.y-BRICKSIZE.y*2) )

	renderer.draw_rect( (0, 0, WINDOW_SIZE.x, UPPER_MARGIN) )
	renderer.draw_rect( (BRICKSIZE.x, WINDOW_SIZE.y-LOWER_MARGIN, WINDOW_SIZE.x - 2*BRICKSIZE.x, LOWER_MARGIN) )

	renderer.draw_rect( gameSpace(), color=(0xff, 0, 0, 0xff) )

#------------------------------

def loadTextures(renderer):
	sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

	Palette.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("palette.bmp"))
	Ball.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("ball.png"))
	Brick.TEXTURES = {
		Brick.REGULAR : sprite_factory.from_image(RESOURCES.get_path("brick.bmp")),
		Brick.INVULNERABLE : sprite_factory.from_image(RESOURCES.get_path("invulnerable.bmp"))
	}

def run():
	# Initialization.
	sdl2.ext.init()

	window = sdl2.ext.Window("pyNoid", size=tuple(WINDOW_SIZE), position=None, flags=sdl2.SDL_WINDOW_SHOWN)
	renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)

	spriterenderer = sdl2.ext.TextureSpriteRenderSystem(renderer)
	loadTextures(renderer)

	game = level.Level( loader.loadLevel('?') )

	# Main loop.
	is_open = True
	while is_open:

		# Event loop.
		events = sdl2.ext.get_events()
		for e in events:
			game.handleEvent(e)

			if e.type == sdl2.SDL_QUIT:
				is_open = False
				break
			elif e.type == sdl2.SDL_KEYDOWN:
				key = e.key.keysym.sym
				if key == sdl2.SDLK_ESCAPE:
					is_open = False
				break

		# Clear window.
		renderer.clear(color=(0, 0, 0, 0xff))		

		# Game logic.
		game.update()

		# Draw and update window.
		dissectWindow(renderer)
		game.render(renderer)
		renderer.present()

	sdl2.ext.quit()
	return 0


if __name__ == "__main__":
	sys.exit(run())