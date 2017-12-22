#!/usr/bin/python3

import gameinstance
import colour
import text
import sdl2

class Menu(gameinstance.GameInstance):
	"""Game menu representation."""

	def __init__(self, renderer):
		self.choice = None
		self.is_open = True
		self.title = text.Text('pyNoid', renderer, 128)
		#self.sub = text.Text('New game', renderer, 48, colour.Colour.Green)

		self.sub = text.Button(
			text.Text('New Game', renderer, 48, colour.Colour.White),
			text.Text('New Game', renderer, 48, colour.Colour.Green),
			text.Text('New Game', renderer, 48, colour.Colour.greyscale(0.45)),
			(150, 350)
		)

	def update(self):
		"""Update game state."""
		pass

	def handleEvent(self, e):
		"""Process relevant events."""

		self.sub.handleEvent(e)
		if self.sub.state == text.Button.PRESSED:
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