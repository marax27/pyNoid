#!/usr/bin/python3

import sys
import dev
import math
import sdl2.ext
import sdl2.sdlttf
import level
import loader
from colour import Colour
from constants import *
from gameobject import Ball, Palette, Brick

from vec2 import vec2

#------------------------------

def run(file = None):
	# Initialization.
	sdl2.ext.init()
	#sdl2.sdlttf.TTF_Init()

	if file is not None:
		unpacked_log = dev.unpack(file)
		for i in unpacked_log:
			print("<{}>".format(i))

	window = sdl2.ext.Window("pyNoid", size=tuple(WINDOW_SIZE), position=None, flags=sdl2.SDL_WINDOW_SHOWN)
	renderer = sdl2.ext.Renderer(window, flags=sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)

	spriterenderer = sdl2.ext.TextureSpriteRenderSystem(renderer)
	loader.loadTextures(renderer)

	game = level.Level( loader.loadLevel('levels/p1.noid') )

	#font_kremlin = sdl2.sdlttf.TTF_OpenFont(b'resources/kremlin.ttf', FONT_SIZE_1)
	#text_surf = sdl2.sdlttf.TTF_RenderText_Solid(font_kremlin, b'God is dead, government is lame.', sdl2.SDL_Color(*Colour.White))

	font_manager = sdl2.ext.FontManager('resources/kremlin.ttf', size=FONT_SIZE_1)
	surf1 = font_manager.render('GOD IS DEAD, GOVERNMENT IS LAME.')
	texture1 = sdl2.SDL_CreateTextureFromSurface(renderer.renderer, surf1)
	w, h = surf1.w, surf1.h

	#sf = sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
	#txtr1 = sf.from_surface(surf1)
	#tsrs = sdl2.ext.TextureSpriteRenderSystem(renderer)

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
		dev.dissectWindow(renderer)
		game.render(renderer)

		#tsrs.render(txtr1)
		sdl2.SDL_RenderCopy(renderer.renderer, texture1, None, sdl2.SDL_Rect(0,0,w,h))

		renderer.present()

	sdl2.ext.quit()
	#sdl2.sdlttf.TTF_CloseFont(font_kremlin)
	#sdl2.sdlttf.TTF_Quit()
	return 0


if __name__ == "__main__":
	args = sys.argv
	if len(args) == 2:
		sys.exit(run(args[1]))
	else:
		sys.exit(run())