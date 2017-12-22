#!/usr/bin/python3

import gameinstance
import colour
import text
import sdl2

class Menu(gameinstance.GameInstance):
	"""Game menu representation."""

	def __init__(self):
		self.choice = None
		self.is_open = True

	def update(self):
		"""Update game state."""
		pass

	def handleEvent(self, e):
		"""Process relevant events."""
		if e.type == sdl2.SDL_MOUSEBUTTONDOWN:
			if e.button.button == sdl2.SDL_BUTTON_RIGHT:
				self.choice = 'levels/p1.noid'

	def render(self, renderer):
		"""Render scene."""
		title = text.Text('pyNoid', renderer, 128)
		sub = text.Text('New game', renderer, 48, colour.Colour.Green)
		title.render(renderer, (200, 200))
		sub.render(renderer, (150, 350))

	def isOpen(self):
		"""Returns False if GameInstance should be no longer active."""
		return self.is_open