#!/usr/bin/python3

import gameinstance
from colour import Colour
import sdl2
import hud

class Menu(gameinstance.GameInstance):
	"""Game menu representation."""

	def __init__(self, renderer):
		self.choice = None
		self.is_open = True
		self.title = hud.Text('pyNoid', renderer, 128)

		self.sub = hud.Button.buildClickableText(
			'New Game', renderer,
			Colour.White, Colour.Green, Colour.greyscale(0.75), (150, 350)
		)

	def update(self):
		"""Update game state."""
		pass

	def handleEvent(self, e):
		"""Process relevant events."""

		self.sub.handleEvent(e)
		if self.sub.state == hud.Button.PRESSED:
			self.choice = 'levels/p1.noid'

		#if e.type == sdl2.SDL_MOUSEBUTTONDOWN:
		#	if e.button.button == sdl2.SDL_BUTTON_RIGHT:
		#		self.choice = 'levels/p1.noid'

	def render(self, renderer):
		"""Render scene."""
		self.title.render(renderer, (200, 200))
		self.sub.render(renderer)

	def isOpen(self):
		"""Returns False if GameInstance should be no longer active."""
		return self.is_open