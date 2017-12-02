#!/usr/bin/python3

class Colour:
	"""Contains RGB definitions of several colours,
	as well as helper functions.
	Should ease a use of colours in rendering functions and so forth."""

	# Color definitions.
	White = 0xff, 0xff, 0xff, 0xff
	Black = 0, 0, 0, 0xff
	Red   = 0xff, 0, 0, 0xff
	Green = 0, 0xff, 0, 0xff
	Blue  = 0, 0, 0xff, 0xff

	def greyscale(percent):
		"""Returns a specific shade of gray (unrelated)."""
		if 0.0 <= percent <= 1.0:
			gs = percent * 0xff
			return (gs, gs, gs, 0xff)
		raise ValueError("Value from range [0, 1] is required.")
	

	