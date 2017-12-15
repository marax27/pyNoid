#!/usr/bin/python3

import sdl2.sdlttf
import sdl2.ext
import sdl2

class Text:
	def __init__(self, text, font_manager, renderer):
		surf = font_manager.render(text)
		self.size = (surf.w, surf.h)
		self.position = (0, 0)
		self.texture = sdl2.SDL_CreateTextureFromSurface(renderer.renderer, surf)
	
	def render(self, renderer):
		r = sdl2.SDL_Rect(self.position[0], self.position[1],
		                  self.size[0], self.size[1])
		sdl2.SDL_RenderCopy(renderer.renderer, self.texture, None, r)