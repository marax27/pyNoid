#!/usr/bin/python3

import sys
import math
import sdl2.ext

import vec2

level = [
	[0, 1, 1, 1, 2],
	[0, 0, 2, 0, 0],
	[0, 2, 0, 2, 0],
	[0, 1, 2, 1, 0]
]

BRICK_COLOUR = (0x22, 0x22, 0x99, 0xff)
INVUL_COLOUR = (0xf4, 0xbf, 0x42, 0xff)

TILES = (15, 20)  # How many tiles/bricks should fit into a window.
BRICKSIZE = (85, 30)  # Size (in pixels) of a single brick.
SIDE_MARGIN = BRICKSIZE[0]  # Left and right side of the brick field.
UPPER_MARGIN = 80
LOWER_MARGIN = 80

ADDITIONAL = (SIDE_MARGIN*2, UPPER_MARGIN+LOWER_MARGIN)  # Since window contains not only bricks.
WINSIZE = (BRICKSIZE[0]*TILES[0] + ADDITIONAL[0], BRICKSIZE[1]*TILES[1] + ADDITIONAL[1])  # Total window size.

"""Palette class"""
class Palette:
	HEIGHT = 30
	COLOR = (0x77, 0x77, 0x77, 0xff)
	SPEED = 20

	def __init__(self):
		self.x = int(WINSIZE[0] * 0.25)
		self.y = WINSIZE[1] - self.HEIGHT - 10
		self.width = 200
	
	def rect(self):
		return self.x, self.y, self.width, self.HEIGHT

	def move(self, direction):
		new_x = self.x + direction * self.SPEED
		if new_x < 0:
			new_x = 0
		elif new_x >= WINSIZE[0] - self.width:
			new_x = WINSIZE[0] - self.width
		self.x = new_x

"""Ball class"""
class Ball:
	RADIUS = 15
	SPEED = 3.0

	def __init__(self, x, y, binding=None):
		self.x = x
		self.y = y
		self.velocity = 0.0, 0.0
		self.binding = binding  # If a ball lies upon a palette, binding represents
		                        # the palette. If ball flies, binding=None.
	
	def render(self, renderer):
		_x, _y = int(self.x), int(self.y)
		renderer.draw_line((_x - self.RADIUS, _y, _x + self.RADIUS, _y), (0xff, 0xff, 0xff, 0xff))
		renderer.draw_line((_x, _y - self.RADIUS, _x, _y + self.RADIUS), (0xff, 0xff, 0xff, 0xff))

	def update(self, dt):
		if self.attached is None:
			self.x += self.SPEED[0] * dt
			self.y += self.SPEED[1] * dt
		else:


#------------------------------
def brickToScreenCoords(x, y):
	return x * BRICKSIZE[0] + SIDE_MARGIN, y * BRICKSIZE[1] + UPPER_MARGIN

def physicalToScreenCoords(x, y):
	return NotImplemented
#------------------------------
def brickCoordsToRect(x, y):
	return brickToScreenCoords(x, y) + BRICKSIZE

def drawGrid(renderer, color=(0x44, 0x44, 0x44, 0xff)):
	renderer.color = color
	for i in range(0, TILES[0]):
		for j in range(0, TILES[1]):
			renderer.draw_rect( brickCoordsToRect(i, j) )
#------------------------------

def run():
	sdl2.ext.init()
	RESOURCES = sdl2.ext.Resources(__file__, "resources")

	window = sdl2.ext.Window("Hello world!", size=WINSIZE, position=None, flags=sdl2.SDL_WINDOW_SHOWN)

	renderer = sdl2.ext.Renderer(window, index=-1, logical_size=None, flags=sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)
	# factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
	# spriterenderer = sdl2.ext.TextureSpriteRenderSystem(renderer)

	palette = Palette()
	ball = Ball(WINSIZE[0]//2, WINSIZE[1] - 80)

	is_open = True
	while is_open:
		events = sdl2.ext.get_events()
		for e in events:
			if e.type == sdl2.SDL_QUIT:
				is_open = False
				break
			elif e.type == sdl2.SDL_KEYDOWN:
				key = e.key.keysym.sym
				if key == sdl2.SDLK_LEFT:
					palette.move(-1)
				elif key == sdl2.SDLK_RIGHT:
					palette.move(+1)
				elif key == sdl2.SDLK_ESCAPE:
					is_open = False
				break

		renderer.clear(color=(0, 0, 0, 0xff))		
		#spriterenderer.render(brick_sprite)

		drawGrid(renderer)

		for i,tab in enumerate(level):
			for j,_id in enumerate(tab):
				if _id == 1:
					renderer.fill(brickCoordsToRect(i, j), BRICK_COLOUR)
				elif _id == 2:
					renderer.fill(brickCoordsToRect(i, j), INVUL_COLOUR)
		
		renderer.fill(palette.rect(), palette.COLOR)
		ball.render(renderer)
		renderer.present()

		ball.update(2.5)

	sdl2.ext.quit()
	return 0


if __name__ == "__main__":
	sys.exit(run())