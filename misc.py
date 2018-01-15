import sdl2
import sdl2.ext
import ctypes
from constants import Constants
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
	return (Constants.SIDE_MARGIN,
	        0, #UPPER_MARGIN,
		    Constants.WINDOW_SIZE.x - 2 * Constants.SIDE_MARGIN,
		    Constants.WINDOW_SIZE.y ) #- UPPER_MARGIN)

class Fade():
	MAXIMUM = 50
	DARKEN, LIGHTEN = 0x998, 0x999

	def __init__(self, darken=True):
		self.reset(darken)
	
	def getState(self):
		if self.state < Fade.MAXIMUM:
			self.state += 1
			return self.state - 1
		return self.state

	def getColour(self):
		a = int(0xff * self.getState() / Fade.MAXIMUM)
		if a == Fade.LIGHTEN:
			a = 0xff - a
		return (0, 0, 0, a)
	
	def finished(self):
		return self.state == Fade.MAXIMUM

	def reset(self, darken=True):
		self.state = 0
		self.direction = Fade.DARKEN if darken else Fade.LIGHTEN

	def draw(self, renderer):
		renderer.fill((0, 0, Constants.WINDOW_SIZE.x, Constants.WINDOW_SIZE.y), color=self.getColour())