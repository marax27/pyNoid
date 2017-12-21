#!/usr/bin/python3

from constants import FONT_SIZE_1
import sdl2.sdlttf
import sdl2.ext
import sdl2

class Text:
	font_manager = sdl2.ext.FontManager('resources/vga_437.ttf', size=FONT_SIZE_1)

	def __init__(self, text, renderer, size=None, color=None):
		self.position = (0, 0)
		self.load(text, renderer, size, color)
	
	def render(self, renderer, pos=None):
		r = sdl2.SDL_Rect(self.position[0] if not pos else pos[0],
		                  self.position[1] if not pos else pos[1],
		                  self.size[0],
		                  self.size[1])
		sdl2.SDL_RenderCopy(renderer.renderer, self.texture, None, r)

	def load(self, text, renderer, size=None, color=None):
		surf = Text.font_manager.render(text, size=size, color=color)
		self.size = (surf.w, surf.h)
		self.texture = sdl2.SDL_CreateTextureFromSurface(renderer.renderer, surf)