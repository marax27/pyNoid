#!/usr/bin/python3
from misc import Fade

class GameInstance:
	"""A base class for classes that represent some game state."""

	fader = Fade()
	fading = False

	def update(self):
		"""Update game state."""
		pass

	def handleEvent(self, e):
		"""Process relevant events."""
		pass

	def render(self, renderer):
		"""Render scene."""
		pass
	
	def isOpen(self):
		"""Returns False if GameInstance should be no longer active."""
		pass
	
	def typeOf(self):
		return 'GameInstance'

#--------------------------------------------------
