#!/usr/bin/python3

import sys
import dev
import math
import sdl2.ext
import sdl2.sdlttf
import level
import menu
import loader
from colour import Colour
from constants import Constants
from gameobject import Ball, Palette, Brick

from vec2 import vec2

#------------------------------

def run(file = None):
	# Initialization.
	sdl2.ext.init()
	#Constants.init((1300, 700))

	if file is not None:
		unpacked_log = dev.unpack(file)
		for i in unpacked_log:
			print("<{}>".format(i))
	
	loader.readConfig()

	if Constants.IS_FULLSCREEN:
		print('Fullscreen')
		flags = sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP
	else:
		flags = sdl2.SDL_WINDOW_SHOWN

	window = sdl2.ext.Window("pyNoid", size=tuple(Constants.WINDOW_SIZE), position=None, flags=flags)
	renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)
	renderer.blendmode = sdl2.SDL_BLENDMODE_BLEND

	# In case of fullscreen mode.
	Constants.WINDOW_SIZE = vec2(window.size[0], window.size[1])

	# Scale game objects.
	Ball.RADIUS *= Constants._scale_ratio
	Ball.RADIUS = int(Ball.RADIUS)	
	Palette.SIZE *= Constants._scale_ratio
	Palette.SIZE = vec2(int(Palette.SIZE.x), int(Palette.SIZE.y))

	loader.loadTextures(renderer)

	#game = level.Level( loader.loadLevel('levels/p1.noid') )
	main_menu = menu.Menu(renderer)
	instance = main_menu

	# Main loop.
	is_open = True
	while main_menu.isOpen() and is_open:

		# Event loop.
		events = sdl2.ext.get_events()
		for e in events:
			instance.handleEvent(e)
			dev.handleEvent(e, instance)

			if e.type == sdl2.SDL_QUIT:
				is_open = False
				break
			#elif e.type == sdl2.SDL_KEYDOWN:
			#	key = e.key.keysym.sym
			#	if key == sdl2.SDLK_ESCAPE:
			#		is_open = False
			#	break

		# Clear window.
		renderer.clear(color=Colour.Black)

		# Game logic.
		#game.update()
		instance.update()

		if instance is main_menu and main_menu.choice is not None:
			instance = level.Level( loader.loadLevel(main_menu.choice) )
			main_menu.choice = None
			sdl2.SDL_ShowCursor(False)
			continue

		if instance is not main_menu and not instance.isOpen():
			instance = main_menu  #TODO
			sdl2.SDL_ShowCursor(True)

		# Draw and update window.
		#dev.dissectWindow(renderer)
		instance.render(renderer)
		renderer.present()

	sdl2.ext.quit()
	return 0

#------------------------------

if __name__ == "__main__":
	args = sys.argv
	if len(args) == 2:
		sys.exit(run(args[1]))
	else:
		sys.exit(run())