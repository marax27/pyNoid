#!/usr/bin/python3

from gameobject import Brick, Palette, Ball, Wall, Bonus
from vec2 import vec2, intmatch
import sdl2.ext
import io
import re

RESOURCES = sdl2.ext.Resources(__file__, "resources")

class NoidError(IOError):
	pass

def loadLevel(filename):
	"""Returns array of bricks that makes a level."""
	
	result = []
	with io.open(filename, 'r') as reader:
		# Get all lines from file, and remove newline character from end.
		lines = [ x[:-1] for x in reader.readlines() ]
		lines.remove('')  #remove empty lines
		
		# Split each line into tokens.
		tokens = [ x.split(' ') for x in lines ]

		brick_types = {
			"regular": Brick.REGULAR, "heavy": Brick.HEAVY,
			"heavier": Brick.HEAVIER, "invulnerable": Brick.INVULNERABLE
		}

		for line in tokens:
			# Very unlikely, empty lines removal should deal with it.
			if len(line) == 0:
				continue

			# A line content is determined by its first token.
			line_type = line[0]
			if len(line_type) == 0 or line_type[0] == "#":
				# Comment - to omit.
				continue
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
							brick = Brick(pos, brick_types[line_type])
							result.append(brick)
	return result 

def loadTextures(renderer):
	"""Load necessary textures from drive."""
	sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

	Palette.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("palette.bmp"))
	Ball.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("ball.png"))
	Brick.TEXTURES = {
		Brick.REGULAR: sprite_factory.from_image(RESOURCES.get_path("brick.png")),
		Brick.INVULNERABLE: sprite_factory.from_image(RESOURCES.get_path("invulnerable.png")),
		Brick.HEAVY: sprite_factory.from_image(RESOURCES.get_path("heavy.bmp")),
		Brick.HEAVIER: sprite_factory.from_image(RESOURCES.get_path("heavier.bmp"))
	}

	Wall.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("wall.png"))
	Bonus.TEXTURE = sprite_factory.from_image(RESOURCES.get_path("p.png"))
