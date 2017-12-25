import sdl2
import sdl2.ext
import ctypes
import constants
from random import random, randrange

def getMousePos():
	"""Obtain current mouse position."""
	x, y = ctypes.c_int(0), ctypes.c_int(0)
	sdl2.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
	return (x.value, y.value)

def randomBool(probability):
	"""probability should belong to interval [0, 1]."""
	return random() < probability

def randomDict(d):
	"""Returns random weighted dict record. Values are assumed to be weights."""
	total_weight = sum(d.values())
	r = randrange(total_weight)
	pos = 0
	for k,v in d.items():
		if pos <= r < pos+v:
			return k
		else:
			pos += v
	raise ValueError('Unexpected end of loop.')

def randomWithWeights(values, weights):
	length = len(values)
	if length != len(weights):
		raise ValueError()
	total_weight = sum(weights)
	r = randrange(total_weight)
	pos = 0
	for i in range(length):
		if pos <= r < pos+weights[i]:
			return values[i]
		else:
			pos += weights[i]

def gameSpace():
	"""Returns the rectangle within which the game 'runs'."""
	return (constants.SIDE_MARGIN,
	        0, #UPPER_MARGIN,
		    constants.WINDOW_SIZE.x - 2 * constants.SIDE_MARGIN,
		    constants.WINDOW_SIZE.y ) #- UPPER_MARGIN)
