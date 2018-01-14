#!/usr/bin/python3

import gameinstance
from colour import Colour
from constants import Constants
from vec2 import vec2
from misc import Fade
import sdl2
import hud

class Menu(gameinstance.GameInstance):
	"""Game menu representation."""

	def __init__(self, renderer, highscores=None):
		self.choice = None
		self.is_open = True

		self.title = hud.Text('pyNoid', renderer, Constants.TITLE_FONT_SIZE)
		self.title.position = vec2(50, 50)

		grey = Colour.greyscale(0.75)

		sub1 = hud.Button.buildClickableText('New Game', renderer,
			Colour.White, grey, grey, Constants.MENU_FONT_SIZE
		)
		sub2 = hud.Button.buildClickableText('Exit', renderer,
			Colour.White, grey, grey, Constants.MENU_FONT_SIZE
		)
		self.menu = hud.VerticalContainer([sub1, sub2], Constants.WINDOW_SIZE.y//2)

		if highscores:
			leaderboard = []
			player_name_length = max([len(x[0]) for x in highscores])
			s_format = '{:>%d} {}' % player_name_length
			for i in highscores:
				leaderboard.append( hud.Text(s_format.format(i[0], i[1]), renderer, Constants.FONT_SIZE_1) )
			for idx,text in enumerate(leaderboard):
				text.position = vec2(
					int(Constants.WINDOW_SIZE.x - 400*Constants._scale_ratio),
					int(400*Constants._scale_ratio + idx*Constants.FONT_SIZE_1))
			self.render_content = leaderboard
		else:
			self.render_content = []

	def update(self):
		"""Update game state."""
		pass

	def handleEvent(self, e):
		"""Process relevant events."""
		for i in self.menu.elem:
			i.handleEvent(e)

		if self.menu.elem[0].isPressed():
			self.fading = True
		elif self.menu.elem[1].isPressed():
			self.is_open = False
	
	def render(self, renderer):
		"""Render scene."""
		self.title.render(renderer)
		self.menu.render(renderer)
		for i in self.render_content:
			i.render(renderer)
		if self.fading:
			self.fader.draw(renderer)
			if self.fader.finished():
				self.fading = False
				self.fader.reset()
				self.choice = 0

	def isOpen(self):
		"""Returns False if GameInstance should be no longer active."""
		return self.is_open

	def typeOf(self):
		return 'Menu'