#!/usr/bin/python3

from gameobject import Ball, Palette, Brick, Wall, Bonus
from collision import *
from vec2 import *
import gameinstance
import constants
import misc
import sdl2
import hud

class Level(gameinstance.GameInstance):
	"""A single level representation."""

	# Reasons to end/restart the level.
	DEATH      = 0x1234
	NEXT_LEVEL = 0x1235
	QUIT_LEVEL = 0x1236

	class Score:
		BRICK_HIT   = 10
		PICKUP      = 20
		GOOD_PICKUP = 20
		BAD_PICKUP  = -20
		# TODO

	def __init__(self, bricks):
		self.endgame = False
		self.score = 0
		self.lives = 3
		self.bonuses = []		
		self.palette = Palette()
		self.bricks  = bricks
		self.ball    = Ball(vec2(0, 0), vec2(0, 1), self.palette)
		self.break_reason = None

		mx, my = misc.getMousePos()
		self.palette.setPosition(mx)

		# Bonus-related flags.
		self.catch_n_hold = False
		self.skyfall = False

	def update(self):
		"""Update game state."""
		# 1. Update objects' positions.
		self.ball.update()
		for i in self.bonuses:
			i.update()

		# Remove bricks that exploded at previous frame.
		self.bricks = [x for x in self.bricks if x.brick_type != Brick.EXPLOSION_VICTIM]
		
		# 2. Check for collisions.
		#          WALLS BALL PALETTE BONUSES BRICKS
		#   WALLS    0    1     1       1       0
		#    BALL    1    0     1       0       1
		# PALETTE    1    1     0       1       0
		# BONUSES    1    0     1       0       0
		#  BRICKS    0    1     0       0       0
		#
		# a)ball-wall        circle-box
		# b)ball-palette     circle-box
		# c)ball-bricks      circle-box
		# d)wall-palette     box-box
		# e)wall-bonuses     box-box
		# f)bonuses-palette  box-box
	
		bpos = self.ball.position
		r = self.ball.RADIUS

		# 2a)
		MAGIC = 14  #lowers the 'death zone', so that the game doesn't stop
		            #immediately as ball hits the bottom of the window. 
		gs = misc.gameSpace()
		self.ball.handleCollision(circleLineCollision(bpos, r, x=gs[0]))
		self.ball.handleCollision(circleLineCollision(bpos, r, y=gs[1]))
		self.ball.handleCollision(circleLineCollision(bpos, r, x=gs[0]+gs[2]))
		if(circleLineCollision(bpos, r, y=gs[1]+gs[3]+MAGIC) != NO_COLLISION):
			self.performBreak(self.DEATH)

		# 2b)
		c = circleBoxCollision(bpos, r, self.palette.rect())
		if c != NO_COLLISION:
			self.handleBallPaletteCollision(c)
		
		# 2c)

		# hit_bricks: contains (brick, collision type) information.
		# to_delete: list of bricks to be removed.
		# scored: number of hits that should increase the score.
		hit_bricks, to_delete = [], []
		scored = 0

		for i in self.bricks:
			c = circleBoxCollision(bpos, r, i.rect())
			if c == NO_COLLISION:
				continue

			# Collision ball-brick confirmed.
			hit_bricks.append( (i, c) )

			prev_type = i.brick_type
			i.handleCollision()
			if i.brick_type == Brick.EMPTY:
				if prev_type == Brick.EXPLOSIVE:
					ei = set(self.explosionImpact(i))
					for i in ei:
						i.brick_type = Brick.EXPLOSION_VICTIM
					#to_delete += ei
					#scored += len(ei)
				else:
					to_delete.append(i)
					scored += 1
			
			if len(hit_bricks) > 1:
				break
		
		if len(hit_bricks) < 2:
			for i in hit_bricks:
				self.ball.handleCollision(i[1])
		elif int(hit_bricks[0][0].position.y) == int(hit_bricks[1][0].position.y):
			self.ball.handleCollision(Y_AXIS_COLLISION)
		elif int(hit_bricks[0][0].position.x) == int(hit_bricks[1][0].position.x):
			self.ball.handleCollision(X_AXIS_COLLISION)
		else:
			self.ball.handleCollision(CORNER_NEG_COLLISION)

		#for i, j in hit_bricks:
		#	if i.brick_type != Brick.INVULNERABLE:
		self.score += self.Score.BRICK_HIT * scored

		#Spawning a bonus.
		for i in to_delete:
			if misc.randomBool(constants.BONUS_SPAWN_CHANCE):
				bonus = Bonus(i.center())
				self.bonuses.append(bonus)

		if len(to_delete):
			# Remove destroyed bricks.
			self.bricks = [x for x in self.bricks if x not in to_delete]

			# Check whether player destroyed all the blocks.
			if not len([x for x in self.bricks if x.brick_type != Brick.INVULNERABLE]):
				self.performBreak(self.NEXT_LEVEL)

		# 2d)
		p_x = self.palette.position.x
		if p_x < gs[0]:
			self.palette.position.x = gs[0]
		elif p_x + self.palette.SIZE.x > gs[0] + gs[2]:
			self.palette.position.x = gs[0] + gs[2] - self.palette.SIZE.x

		MAGIC1 = 64
		to_delete, to_handle = [], []
		for i in self.bonuses:
			# 2e)
			r = i.rect()
			i.handleCollision(boxLineCollision(r, x=gs[0]))
			i.handleCollision(boxLineCollision(r, y=gs[1]))
			i.handleCollision(boxLineCollision(r, x=gs[0]+gs[2]))
			if boxLineCollision(r, y=gs[1]+gs[3]+MAGIC1) != NO_COLLISION:
				to_delete.append(i)
			
			# 2f)
			c = boxBoxCollision(i.rect(), self.palette.rect())
			if c:
				to_handle.append(i)
		
		# Handle pickups that have been caught.
		for i in to_handle:
			self.handleBonus(i.type)

		# Remove pickups that were caught or fell down.
		self.bonuses = [x for x in self.bonuses if (x not in to_delete and x not in to_handle)]

		# If the ball somehow escaped, restart the game.
		dist = (self.ball.position - self.palette.position).length()
		if dist > 5000:
			self.performBreak(self.DEATH)

	def handleEvent(self, e):
		"""Process events such as palette movement."""
		
		if e.type == sdl2.SDL_MOUSEMOTION:
			# Since palette is considered unstoppable force, if palette now
			# covers space occupied by the ball, the ball must bend.

			x = e.motion.x
			self.palette.setPosition(x)

			c = circleBoxCollision(self.ball.position, self.ball.RADIUS, self.palette.rect())
			if c != NO_COLLISION:
				#self.ball.position.y = self.palette.position.y - 2*self.ball.RADIUS
				r = self.ball.RADIUS
				bx, px = self.ball.position.x + r, self.palette.position.x
				gs = misc.gameSpace()
				if bx < px + r and px > gs[0] + 2*r:
					# Shift left.
					self.ball.position.x = px - 2*r
				elif bx>px + self.palette.SIZE.x-r and px+self.palette.SIZE.x < gs[0]+gs[2]-2*r:
					# Shift right.
					self.ball.position.x = px + self.palette.SIZE.x
				else:
					# Shift up.
					self.ball.position.y = self.palette.position.y - 2*r

		elif e.type == sdl2.SDL_MOUSEBUTTONDOWN:
			if e.button.button == sdl2.SDL_BUTTON_LEFT:
				self.ball.handleMouseKey()
				
		elif e.type == sdl2.SDL_KEYDOWN:
			key = e.key.keysym.sym
			if key == sdl2.SDLK_ESCAPE:
				self.endgame = True

		# Deprecated: moving palette with a keyboard.
		"""if e.type == sdl2.SDL_KEYDOWN:
			key = e.key.keysym.sym
			if key == sdl2.SDLK_LEFT:
				self.palette.move(-1)
			elif key == sdl2.SDLK_RIGHT:
				self.palette.move(+1)"""

	def handleBonus(self, bonus_type):
		ss = self.Score.PICKUP
		prev_palette_width = Palette.SIZE.x
		
		if bonus_type == Bonus.EXTRA_LIFE:
			ss += self.Score.GOOD_PICKUP
			self.lives += 1
		elif bonus_type == Bonus.TECH_SUPPORT:
			ss += self.Score.GOOD_PICKUP
			pass
		elif bonus_type == Bonus.WIDER_PALETTE:
			Palette.SIZE.x *= 2
			gs = misc.gameSpace()
			if Palette.SIZE.x > gs[2]:
				Palette.SIZE.x = gs[2]
			if self.palette.position.x + Palette.SIZE.x > gs[0]+gs[2]:
				self.palette.position.x -= self.palette.position.x+self.palette.SIZE.x-gs[0]-gs[2]
		elif bonus_type == Bonus.NARROWER_PALETTE:
			Palette.SIZE.x //= 2
		elif bonus_type == Bonus.SUPER_SPEED:
			Ball.SPEED *= 2
		elif bonus_type == Bonus.STRIKE_THROUGH:
			pass
		elif bonus_type == Bonus.FIREBALL:
			pass
		elif bonus_type == Bonus.DEATH:
			ss += self.Score.BAD_PICKUP
			self.performBreak(self.DEATH)
		elif bonus_type == Bonus.SKYFALL:
			self.skyfall = True
		elif bonus_type == Bonus.CATCH_N_HOLD:
			self.catch_n_hold = True
		
		self.score += ss

		# If ball is tied to the palette, adjust ball's position.
		if prev_palette_width != Palette.SIZE.x and self.ball.binding:
			a = self.ball.position.x - self.palette.position.x
			self.ball.position.x = self.palette.position.x + Palette.SIZE.x / prev_palette_width * a
	
	def handleBallPaletteCollision(self, collision_type):
		if self.skyfall:
			self.performSkyfall()
	
		if self.catch_n_hold:
			if not self.ball.binding:
				self.ball.binding = self.palette
				self.ball.offset = self.ball.position.x -self.palette.position.x #+ self.ball.RADIUS - self.palette.position.x
		else:
			self.ball.handlePaletteCollision(collision_type, self.palette)

	def render(self, renderer):
		"""Render the level."""
		renderer.copy(Wall.TEXTURE, None, (0, 0, constants.SIDE_MARGIN, constants.WINDOW_SIZE.y))
		renderer.copy(Wall.TEXTURE, None, (constants.WINDOW_SIZE.x-constants.SIDE_MARGIN, 0, constants.SIDE_MARGIN, constants.WINDOW_SIZE.y))

		self.palette.render(renderer)
		if not self.endgame:
			self.ball.render(renderer)
		for i in self.bricks:
			i.render(renderer)
		for j in self.bonuses:
			j.render(renderer)

		h = hud.Text(str(self.score), renderer, size=constants.UPPER_MARGIN-10)
		h.render(renderer, (constants.SIDE_MARGIN + 50, 5))

		h.load(str(self.lives), renderer, size=constants.UPPER_MARGIN-10)
		h.render(renderer, (constants.WINDOW_SIZE.x - constants.SIDE_MARGIN - 80, 5))

		if self.fading:
			self.fader.draw(renderer)
			if self.fader.finished():
				self.fading = False
				self.fader.reset()
				self.completeBreak()

	def performSkyfall(self):
		"""Move all bricks 1 step down."""
		# Organize existing bricks into columns.
		columns = {}  #key: number of column; value - bricks belonging to the column.
		for i in self.bricks:
			k = i.position.x
			if k not in columns.keys():
				columns[k] = []
			columns[k].append(i)
		
		for k,v in columns.items():
			v = sorted(v, key=lambda brick: -brick.position.y)  #minus shall revert the sorting
			# The 0-th element of 'v' is the lowest brick in a column.
			if v[0].position.y < constants.TILES.y-1:
				v[0].position.y += 1
			for i in range(1, len(v)):
				if v[i].position.y != v[i-1].position.y-1:
					v[i].position.y += 1

	def performBreak(self, reason):
		"""Either completed level or death."""
		self.skyfall = False
		self.catch_n_hold = False
		self.fading = True
		self.break_reason = reason

	def completeBreak(self):
		"""Complete break sequence."""
		if self.break_reason == self.DEATH:
			self.lives -= 1
			if self.lives == 0:
				self.endgame = True
			else:
				self.bonuses = []
				self.restart()
		elif self.break_reason == self.NEXT_LEVEL:
			self.endgame = True
		elif self.break_reason == self.QUIT_LEVEL:
			self.endgame = True
	
	# def completeDeath(self):
		# """Handle ball death sequence. Result depends on an amount of lives player has."""
		# self.lives -= 1
		# if self.lives == 0:
			# self.endgame = True
		# else:
			# self.bonuses = []
			# self.restart()
	# 
	# def performVictory(self):
		# self.performBreak(self.NEXT_LEVEL)
	
	def neighboursOf(self, brick):
		"""Returns list of brick's neighbours."""
		x, y = brick.position.x, brick.position.y
		result = []
		for i in self.bricks:
			if i.position.x == x and i.position.y in (y-1, y+1):
				result.append(i)
				continue
			elif i.position.x in (x-1, x+1) and i.position.y in (y-1, y, y+1):
				result.append(i)
				continue
		return result

	def explosionImpact(self, brick, explosives=[]):
		if explosives == []:
			explosives = [brick]
		neighbours = self.neighboursOf(brick)
		result = neighbours[:]
		for x in [y for y in neighbours if y.brick_type == Brick.EXPLOSIVE and y not in explosives]:
			explosives.append(x)
			result += self.explosionImpact(x, explosives)
		return result

	def restart(self):
		self.ball = Ball(vec2(0, 0), vec2(0, 1), self.palette)

	def isOpen(self):
		"""Returns False if GameInstance should be no longer active."""
		return not self.endgame