#!/usr/bin/python3

import sys
import dev
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

#------------------------------

def run():
	# Initialization.
	sdl2.ext.init()

	window = sdl2.ext.Window("pyNoid", size=tuple(WINDOW_SIZE), position=None, flags=sdl2.SDL_WINDOW_SHOWN)
	renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)

	spriterenderer = sdl2.ext.TextureSpriteRenderSystem(renderer)
	loader.loadTextures(renderer)

	game = level.Level( loader.loadLevel('levels/p1.noid') )
	
	# Main loop.
	is_open = True
	while is_open:

		# Event loop.
		events = sdl2.ext.get_events()
		for e in events:
			game.handleEvent(e)
			dev.handleEvent(e, game)

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
		dev.dissectWindow(renderer)
		game.render(renderer)
		renderer.present()

	sdl2.ext.quit()
	return 0


if __name__ == "__main__":
	sys.exit(run())