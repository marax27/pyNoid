#!/usr/bin/python3

import gameinstance
import sdl2

class Menu(gameinstance.GameInstance):
	"""Game menu representation."""

	def update(self):
		"""Update game state."""
		pass

	def handleEvent(self, e):
		"""Process relevant events."""
		if e.type == sdl2.SDL_MOUSEBUTTONDOWN:
			

	def render(self, renderer):
		"""Render scene."""
		pass