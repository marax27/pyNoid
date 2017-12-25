#!/usr/bin/python3

from vec2 import vec2

"""Width and height of the game board."""
TILES = vec2(18, 20)

"""Size of a single brick."""
BRICKSIZE = vec2(65, 25) #vec2(85, 30)

"""Width of space between the board and left/right window edge."""
SIDE_MARGIN = BRICKSIZE.x

UPPER_MARGIN = BRICKSIZE.y * 2

LOWER_MARGIN = BRICKSIZE.y * 2

"""Size of a pickup."""
BONUS_SIZE = 64

"""Probability of bonus spawning after a brick is destroyed."""
BONUS_SPAWN_CHANCE = 1

"""Duration of a single simulation step."""
DELTA_T = 0.8

"""Gravitational acceleration."""
G_ACCEL = 0.08

"""Font sizes."""
FONT_SIZE_1 = 36
TITLE_FONT_SIZE = 96

"""Total size of a game window."""
WINDOW_SIZE = vec2(
	BRICKSIZE.x * TILES.x + 2*SIDE_MARGIN,
	BRICKSIZE.y * TILES.y + UPPER_MARGIN + LOWER_MARGIN
)