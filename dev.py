#!/usr/bin/python3

import io
import pickle
import sdl2.ext
import gameobject
from vec2 import vec2
from misc import gameSpace
from constants import Constants

"""Development tools."""
DEV_MODE = False

def handleEvent(event, game):
	if not DEV_MODE:
		return

	if event.type == sdl2.SDL_KEYDOWN:
		key = event.key.keysym.sym
		if key == sdl2.SDLK_KP_PLUS:
			gameobject.Ball.SPEED *= 2
		elif key == sdl2.SDLK_KP_MINUS:
			gameobject.Ball.SPEED /= 2
		elif key == sdl2.SDLK_UP:  game.ball.velocity.y -= 0.5;
		elif key == sdl2.SDLK_DOWN:  game.ball.velocity.y += 0.5;
		elif key == sdl2.SDLK_LEFT:  game.ball.velocity.x -= 0.5;
		elif key == sdl2.SDLK_RIGHT:  game.ball.velocity.x += 0.5;
		elif key == sdl2.SDLK_RIGHTBRACKET:
			game.bonuses.append( gameobject.Bonus(Constants.BRICKSIZE * 2) )
		elif key == sdl2.SDLK_LEFTBRACKET:
			exit()
		
		game.ball.velocity = game.ball.velocity.normalized()

def drawGrid(renderer, color=(0x44, 0x44, 0x44, 0xff)):
	renderer.color = color
	for i in range(Constants.TILES.x):
		for j in range(0, Constants.TILES.y):
			renderer.draw_rect( (Constants.SIDE_MARGIN + Constants.BRICKSIZE.x*i, Constants.UPPER_MARGIN + Constants.BRICKSIZE.y*j) + tuple(Constants.BRICKSIZE), color=color )

def dissectWindow(renderer):
	drawGrid(renderer)

	renderer.draw_rect( (0, 0, Constants.SIDE_MARGIN, WINDOW_SIZE.y) )
	renderer.draw_rect( (WINDOW_SIZE.x-Constants.SIDE_MARGIN, 0, Constants.SIDE_MARGIN, WINDOW_SIZE.y) )

	renderer.draw_rect( (Constants.SIDE_MARGIN, 0, WINDOW_SIZE.x-2*Constants.SIDE_MARGIN, Constants.UPPER_MARGIN) )
	renderer.draw_rect( (Constants.BRICKSIZE.x, WINDOW_SIZE.y-Constants.LOWER_MARGIN, WINDOW_SIZE.x - 2*Constants.BRICKSIZE.x, Constants.LOWER_MARGIN) )

	renderer.draw_rect( gameSpace(), color=(0xff, 0, 0, 0xff) )

def dumpable(dump):
	s = str(dump[0])
	for b in dump[1:]:
		s = s + ',' + str(b)
	return s

FIELD_DELIM = b'@!!'
ARG_DELIM = b' '
def report(*args):
	return
	for i in args:
		print('@!!{}@!!{}@!! '.format(str(i).replace(' ', ''), dumpable(pickle.dumps(i))), end='')
	print()

def unpack(log_file):
	with io.open(log_file, 'rb') as f:
		result = []
		lines = f.readlines()
		for line in lines:
			#print('{ ', end='')
			spl = [x for x in line.split(ARG_DELIM) if not x.isspace() and x != b'']
			obj = []

			for arg in spl:
				a = [x for x in arg.split(FIELD_DELIM) if not x.isspace() and x != b'']
				my_bytes = b''
				for i in a[1].split(b','):
					my_bytes = my_bytes + bytes([int(i)])
				value = pickle.loads(my_bytes)

				obj.append(value)
				#print(value, end='; ')
			#print('}')
			result.append(tuple(obj))
		return result

