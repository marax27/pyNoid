#!/usr/bin/python3

from vec2 import vec2

class Constants:
	"""Width and height of the game board."""
	TILES = vec2(18, 24)

	"""Size of a single brick (in game).
	BRICKSIZE = vec2(65, 25) #vec2(85, 30)"""

	"""Size of a single brick texture (in image file)."""
	BRICK_TEXTURESIZE = vec2(200, 80)

	"""Width of space between the board and left/right window edge.
	SIDE_MARGIN = BRICKSIZE.x

	UPPER_MARGIN = BRICKSIZE.y * 2

	LOWER_MARGIN = BRICKSIZE.y * 2"""

	"""Size of a pickup."""
	BONUS_SIZE = 64

	"""Probability of bonus spawning after a brick is destroyed."""
	BONUS_SPAWN_CHANCE = 0.225

	"""Duration of a single simulation step."""
	DELTA_T = 0.8

	"""Gravitational acceleration."""
	G_ACCEL = 0.08

	"""Font sizes.
	FONT_SIZE_1 = 36
	TITLE_FONT_SIZE = 96"""

	"""Total size of a game window.
	WINDOW_SIZE = vec2(
		BRICKSIZE.x * TILES.x + 2*SIDE_MARGIN,
		BRICKSIZE.y * TILES.y + UPPER_MARGIN + LOWER_MARGIN
	)"""

	WINDOW_SIZE  = None
	BRICKSIZE    = None
	SIDE_MARGIN  = None
	UPPER_MARGIN = None
	LOWER_MARGIN = None
	FONT_SIZE_1     = None
	TITLE_FONT_SIZE = None

	@staticmethod
	def init(win_size):
		Constants.WINDOW_SIZE = vec2(int(win_size[0]), int(win_size[1]))

		ratio = 0.5 * (win_size[0]/1300 + win_size[1]/700)

		Constants.BRICKSIZE = vec2(int(65 * ratio), int(25 * ratio))
		Constants.SIDE_MARGIN = int(Constants.BRICKSIZE.x)
		Constants.UPPER_MARGIN = int(Constants.BRICKSIZE.y*2)
		Constants.LOWER_MARGIN = int(Constants.BRICKSIZE.y*2)

		Constants.FONT_SIZE_1 = int(36 * ratio)
		Constants.TITLE_FONT_SIZE = int(96 * ratio)