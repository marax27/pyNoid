#!/usr/bin/python3

class GameInstance:
	"""A base class for classes that represent some game state."""

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

#--------------------------------------------------

