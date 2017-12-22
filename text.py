#!/usr/bin/python3

from constants import FONT_SIZE_1
import sdl2.sdlttf
import sdl2.ext
import sdl2
import ctypes

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

class Button:
	IDLE, HOVER, PRESSED = 0x1001, 0x1002, 0x1003

	def __init__(self, idle_state, pressed_state, hover_state=None, pos=(0,0)):
		self.idle = idle_state
		self.hover = hover_state if hover_state is not None else idle_state
		self.pressed = pressed_state

		self.state = self.IDLE
		self.position = pos

		if self.idle.size != self.hover.size or self.idle.size != self.pressed.size:
			raise ValueError()
		self.size = self.idle.size
	
	def render(self, renderer):
		if self.state == self.PRESSED:
			self.pressed.render(renderer, self.position)
		if self.state == self.HOVER:
			self.hover.render(renderer, self.position)
		else:
			self.idle.render(renderer, self.position)

	def handleEvent(self, event):
		x, y = ctypes.c_int(0), ctypes.c_int(0)
		sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))

		if ((self.position[0] <= x.value < self.position[0] + self.size[0]) and 
		    (self.position[1] <= y.value < self.position[1] + self.size[1])):
			if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
				self.state = self.PRESSED
			else:
				self.state = self.HOVER
		else:
			self.state = self.IDLE

		#hud = Text('x:{}, y:{}'.format(x.value,y.value), renderer, size=constants.UPPER_MARGIN-10)
		#if event.type == sdl2.SDL_MOU