#!/usr/bin/python3

import pickle
import sdl2.ext
import gameobject
from constants import *

"""Development tools."""

def handleEvent(event, game):
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

def drawGrid(renderer, color=(0x44, 0x44, 0x44, 0xff)):
	renderer.color = color
	for i in range(TILES.x):
		for j in range(0, TILES.y):
			pass

def dissectWindow(renderer):
	drawGrid(renderer)

	renderer.draw_rect( (0, BRICKSIZE.y*2, SIDE_MARGIN, WINDOW_SIZE.y-BRICKSIZE.y*2) )
	renderer.draw_rect( (WINDOW_SIZE.x-SIDE_MARGIN, BRICKSIZE.y*2, SIDE_MARGIN, WINDOW_SIZE.y-BRICKSIZE.y*2) )

	renderer.draw_rect( (0, 0, WINDOW_SIZE.x, UPPER_MARGIN) )
	renderer.draw_rect( (BRICKSIZE.x, WINDOW_SIZE.y-LOWER_MARGIN, WINDOW_SIZE.x - 2*BRICKSIZE.x, LOWER_MARGIN) )

	renderer.draw_rect( gameSpace(), color=(0xff, 0, 0, 0xff) )

def report(*args):
	for i in args:
		print('@!!{}@!!{}@!! '.format(i, pickle.dumps(i)), end='')
	print()
