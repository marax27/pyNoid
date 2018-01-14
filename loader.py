#!/usr/bin/python3

from gameobject import Brick, Palette, Ball, Wall, Bonus
from vec2 import vec2, intmatch
from constants import Constants
from colour import Colour
import sdl2.ext
import io
import re

RESOURCES = sdl2.ext.Resources(__file__, "resources")

class NoidError(IOError):
	pass

def readConfig():
	with io.open('config', 'r') as reader:
		lines = [ x[:-1] if x[-1] == '\n' else x for x in reader.readlines() ]
		lines.remove('')  #remove empty lines

		win_size = vec2(-1, -1)

		for line in lines:
			m = re.match('^(.*): (.*)$', line)
			if m:
				gr = m.groups()
				first = gr[0].lower()

				if len(gr) != 2:
					raise NoidError('Invalid config record.')
				if first == 'width':
					win_size.x = int(gr[1])
				elif first == 'height':
					win_size.y = int(gr[1])
				elif first == 'fullscreen':
					Constants.IS_FULLSCREEN = (gr[1] in ['True', 'true', '1'])
				elif first == 'levels':
					Constants.LEVELS = gr[1].split()

		Constants.init(win_size)
		
def readHighscores():
	result = []
	with io.open('highscores', 'r') as reader:
		lines = [x.split() for x in reader.readlines()]
		for i in lines:
			if len(i) != 2:
				print("Invalid record in 'highscores'")
				continue
			result.append( (i[0] if i[0]!='*' else '', i[1]) )
	return result

def loadLevel(filename):
	"""Returns array of bricks that makes a level."""
	
	result = []
	with io.open(filename, 'r') as reader:
		# Get all lines from file, and remove newline character from end.
		lines = [ x[:-1] if x[-1] == '\n' else x for x in reader.readlines() ]
		lines = [x for x in lines if x != '']  #remove empty lines
		
		# Split each line into tokens.
		tokens = [ x.split(' ') for x in lines ]

		brick_types = {
			"regular": Brick.REGULAR, "heavy": Brick.HEAVY,
			"heavier": Brick.HEAVIER, "invulnerable": Brick.INVULNERABLE,
			"explosive": Brick.EXPLOSIVE
		}
		# Types of bricks that are present in more than one colour.
		COLOURFUL_BRICKS = ('regular', 'heavy', 'heavier')

		for line in tokens:
			# Very unlikely, empty lines removal should deal with it.
			if len(line) == 0:
				continue

			# Line content is determined by its first token.
			if len(line[0]) == 0 or line[0][0] == "#":
				# Line is a comment - to omit.
				continue
			
			decomposition = line[0].split('.')
			if decomposition[0] in COLOURFUL_BRICKS:
				if len(decomposition) != 2:
					raise NoidError('Expected colour.')
			else:
				if len(decomposition) != 1:
					raise NoidError('Too much information.')

			line_type = decomposition[0]
			colour = None
			if line_type in COLOURFUL_BRICKS:
				line_colour = decomposition[1]
				if line_colour == 'red':
					colour = Brick.Colour.RED
				elif line_colour == 'green':
					colour = Brick.Colour.GREEN
				elif line_colour == 'blue':
					colour = Brick.Colour.BLUE
				else:
					raise NoidError('Unknown colour name: "{}".'.format(line_colour))

			if line_type in brick_types.keys():
				for i in line[1:]:
					# Read brick coordinates and form bricks array.
					# Supported coordinates formats:
					# x,y         : single brick
					# x1-x2,y     : horizontal line of bricks
					# x,y1-y2     : vertical line of bricks
					# x1-x2,y1-y2 : rectangle of bricks

					COORD_DELIM = ','  #coordinates delimiter
					RANGE_DELIM = '-'  #range delimiter

					if i == '':
						continue

					spl = i.split(COORD_DELIM)
					if len(spl) != 2:
						raise NoidError("Invalid coordinates")

					rect = [0, 0, 0, 0]

					# Count number of delimiters on the left and right of coord_delim
					delims = [i.count(RANGE_DELIM) for i in spl]
					for j in (0, 1):
						if delims[j] == 0:
							# Single coordinate.
							rect[2*j] = rect[2*j+1] = int(spl[j])
						elif delims[j] == 1:
							# t1-t2 format detected.
							rect[2*j], rect[2*j+1] = [int(x) for x in spl[j].split(RANGE_DELIM)]
						else:
							# Too many separators (something like 3-2-5,7)
							raise NoidError("Invalid range")
					
					# Append new bricks.
					for x in range(rect[0], rect[1]+1):
						for y in range(rect[2], rect[3]+1):
							pos = vec2(x, y)
							if [i for i in result if intmatch(i.position, pos)]:
								raise NoidError("More than 1 brick occupy exact same space")
							brick = Brick(pos, brick_types[line_type], colour)
							result.append(brick)
	return result 

def loadTextures(renderer):
	"""Load necessary textures from drive."""
	sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

	Palette.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("palette.png"))
	Ball.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("ball.png"))
	Brick.TEXTURES = {
		Brick.REGULAR: sprite_factory.from_image(RESOURCES.get_path("brick_set.png")),
		Brick.INVULNERABLE: sprite_factory.from_image(RESOURCES.get_path("invulnerable.png")),
		Brick.HEAVY: sprite_factory.from_image(RESOURCES.get_path("heavy.png")),
		Brick.HEAVIER: sprite_factory.from_image(RESOURCES.get_path("heavier.png")),
		Brick.EXPLOSIVE: sprite_factory.from_image(RESOURCES.get_path("explosive.png")),
		Brick.EXPLOSION_VICTIM: sprite_factory.from_color(Colour.White, vec2(10, 10))
	}

	Wall.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("wall.png"))
	Bonus.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("p.png"))
