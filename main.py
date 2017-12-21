#!/usr/bin/python3

import sys
import dev
import math
import sdl2.ext
import sdl2.sdlttf
import level
import loader
import text
from colour import Colour
from constants import *
from gameobject import Ball, Palette, Brick

from vec2 import vec2

#------------------------------

def run(file = None):
	# Initialization.
	sdl2.ext.init()
	sdl2.SDL_ShowCursor(False)

	if file is not None:
		unpacked_log = dev.unpack(file)
		for i in unpacked_log:
			print("<{}>".format(i))

	window = sdl2.ext.Window("pyNoid", size=tuple(WINDOW_SIZE), position=None, flags=sdl2.SDL_WINDOW_SHOWN)
	renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)

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
		renderer.clear(color=Colour.Black)

		# Game logic.
		game.update()

		# Draw and update window.
		#dev.dissectWindow(renderer)
		game.render(renderer)

		renderer.present()

	sdl2.ext.quit()
	return 0


if __name__ == "__main__":
	args = sys.argv
	if len(args) == 2:
		sys.exit(run(args[1]))
	else:
		sys.exit(run())