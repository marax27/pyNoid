#!/usr/bin/python3

import gameinstance
from colour import Colour
from constants import WINDOW_SIZE, TITLE_FONT_SIZE
from vec2 import vec2
from misc import Fade
import sdl2
import hud

class Menu(gameinstance.GameInstance):
	"""Game menu representation."""

	def __init__(self, renderer):
		self.choice = None
		self.is_open = True

		self.title = hud.Text('pyNoid', renderer, TITLE_FONT_SIZE)
		self.title.position = vec2(50, 50)

		grey = Colour.greyscale(0.75)

		sub1 = hud.Button.buildClickableText('New Game', renderer,
			Colour.White, grey, grey
		)
		sub2 = hud.Button.buildClickableText('Exit', renderer,
			Colour.White, grey, grey
		)
		self.menu = hud.VerticalContainer([sub1, sub2], WINDOW_SIZE.y//2)

	def update(self):
		"""Update game state."""
		pass

	def handleEvent(self, e):
		"""Process relevant events."""
		for i in self.menu.elem:
			i.handleEvent(e)

		if self.menu.elem[0].isPressed():
			self.fading = True
		elif self.menu.elem[1].isPressed():
			self.is_open = False
	
	def render(self, renderer):
		"""Render scene."""
		self.title.render(renderer)
		self.menu.render(renderer)
		if self.fading:
			self.fader.draw(renderer)
			if self.fader.finished():
				self.fading = False
				self.fader.reset()
				self.choice = 'levels/p1.noid'

	def isOpen(self):
		"""Returns False if GameInstance should be no longer active."""
		return self.is_open