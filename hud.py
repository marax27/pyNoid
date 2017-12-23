#!/usr/bin/python3

from constants import FONT_SIZE_1
import sdl2.sdlttf
import sdl2.ext
import sdl2
import ctypes

class Text:
	"""Single piece of text."""
	font_manager = sdl2.ext.FontManager('resources/vga_437.ttf', size=FONT_SIZE_1)

	def __init__(self, text, renderer, size=None, color=None):
		self.position = (0, 0)
		self.load(text, renderer, size, color)
	
	def render(self, renderer, pos=None):
		"""Render the text, using the renderer."""
		r = sdl2.SDL_Rect(self.position[0] if not pos else pos[0],
		                  self.position[1] if not pos else pos[1],
		                  self.size[0],
		                  self.size[1])
		sdl2.SDL_RenderCopy(renderer.renderer, self.texture, None, r)

	def load(self, text, renderer, size=None, color=None):
		"""Update a Text object."""
		surf = Text.font_manager.render(text, size=size, color=color)
		self.size = (surf.w, surf.h)
		self.texture = sdl2.SDL_CreateTextureFromSurface(renderer.renderer, surf)

class Button:
	"""Button class."""
	IDLE, HOVER, PRESSED = 0x1001, 0x1002, 0x1003

	@staticmethod
	def buildClickableText(message, renderer, idle_color, pressed_color, hover_color, pos=(0,0)):
		"""Generates a text label that will change color according to whether it's pressed or not."""
		return Button(
			Text(message, renderer, 48, idle_color),
			Text(message, renderer, 48, pressed_color),
			Text(message, renderer, 48, hover_color),
			pos
		)

	def __init__(self, idle_state, pressed_state, hover_state=None, pos=(0,0)):
		#self.idle = idle_state
		#self.hover = hover_state if hover_state is not None else idle_state
		#self.pressed = pressed_state
		self.states = {}
		self.states[self.IDLE] = idle_state
		self.states[self.HOVER] = hover_state if hover_state is not None else idle_state
		self.states[self.PRESSED] = pressed_state

		self.state = self.IDLE
		self.position = pos

		# Size restriction.
		if self.states[self.IDLE].size != self.states[self.HOVER].size or self.states[self.IDLE].size != self.states[self.PRESSED].size:
			raise ValueError()
		self.size = self.states[self.IDLE].size

	def render(self, renderer):
		self.states[self.state].render(renderer, self.position)

	def handleEvent(self, event):
		"""Handle mouse events."""
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