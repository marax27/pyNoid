#!/usr/bin/python3

from constants import Constants
from vec2 import vec2
import sdl2.sdlttf
import sdl2.ext
import sdl2
import misc

class UIElement:
	def __init__(self):
		self.position = vec2(0,0)
		self.size = vec2(0,0)
	
	def centerHorizontally(self):
		self.position.x = (Constants.WINDOW_SIZE.x - self.size[0])//2
	
	def centerVertically(self):
		self.position.y = (Constants.WINDOW_SIZE.y - self.size[1])//2

	def center(self):
		self.centerHorizontally()
		self.centerVertically()

class Text(UIElement):
	"""Single piece of text."""
	font_manager = sdl2.ext.FontManager('resources/vga_437.ttf', size=24)

	def __init__(self, text, renderer, size=None, color=None):
		self.position = vec2(0,0)
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

class Button(UIElement):
	"""Button class."""
	IDLE, HOVER, PRESSED = 0x1001, 0x1002, 0x1003

	@staticmethod
	def buildClickableText(message, renderer, idle_color, pressed_color, hover_color, size, pos=None):
		"""Generates a text label that will change color according to whether it's pressed or not."""
		return Button(
			Text(message, renderer, size, idle_color),
			Text(message, renderer, size, pressed_color),
			Text(message, renderer, size, hover_color),
			pos
		)

	def __init__(self, idle_state, pressed_state, hover_state=None, pos=None):
		self.states = {}
		self.states[self.IDLE] = idle_state
		self.states[self.HOVER] = hover_state if hover_state is not None else idle_state
		self.states[self.PRESSED] = pressed_state

		self.state = self.IDLE
		self.position = pos if pos else vec2(0, 0)

		# Size restriction.
		if self.states[self.IDLE].size != self.states[self.HOVER].size or self.states[self.IDLE].size != self.states[self.PRESSED].size:
			raise ValueError()
		self.size = self.states[self.IDLE].size

	def render(self, renderer):
		self.states[self.state].render(renderer, self.position)

	def handleEvent(self, event):
		"""Handle mouse events."""
		mx, my = misc.getMousePos()
		if ((self.position[0] <= mx < self.position[0] + self.size[0]) and 
		    (self.position[1] <= my < self.position[1] + self.size[1])):
			if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
				self.state = self.PRESSED
			else:
				self.state = self.HOVER
		else:
			self.state = self.IDLE
	
	def isPressed(self):
		return self.state == self.PRESSED

class VerticalContainer:
	def __init__(self, elements=[], y_pos=0):
		self.elem = elements
		self.y_pos = y_pos
		self.adjust()
	
	def adjust(self):
		if len(self.elem):
			self.elem[0].position.y = self.y_pos
			for i in range(1, len(self.elem)):
				self.elem[i].position.y = self.elem[i-1].position.y+self.elem[i-1].size[1]
			for i in self.elem:
				i.centerHorizontally()
	
	def render(self, renderer):
		for i in self.elem:
			i.render(renderer)