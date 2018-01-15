#!/usr/bin/python3

import gameinstance
from colour import Colour
from constants import Constants
from vec2 import vec2
from misc import Fade
import sdl2
import hud

class TextGetter(gameinstance.GameInstance):
	"""Simple game instance responsible for getting text data from user."""

	def __init__(self, renderer, message=''):
		self.message = hud.Text(message, renderer, Constants.FONT_SIZE_1)
		self.message.center()

		self.input = ''
		self.is_open = True

	def update(self):
		pass
	
	def handleEvent(self, e):
		if e.type == sdl2.SDL_TEXTINPUT:
			if len(self.input) < 12:
				self.input += e.text.text.decode()
		elif e.type == sdl2.SDL_KEYDOWN:
			key = e.key.keysym.sym
			if key == sdl2.SDLK_RETURN:
				if self.input:
					self.fading = True
			elif key == sdl2.SDLK_BACKSPACE:
				self.input = self.input[:-1] if self.input != '' else ''
			elif key == sdl2.SDLK_ESCAPE:
				self.fading = True
				self.input = ""
	
	def render(self, renderer):
		if self.message:
			self.message.render(renderer)
		if self.input:
			out1 = hud.Text(self.input, renderer, Constants.FONT_SIZE_1)
			out1.position = vec2(self.message.position.x+self.message.size[0], self.message.position[1])
			out1.render(renderer)

		if self.fading:
			self.fader.draw(renderer)
			if self.fader.finished():
				self.fading = False
				self.fader.reset()
				self.is_open = False

	def isOpen(self):
		return self.is_open

	def typeOf(self):
		return 'TextGetter'


#--------------------------------------------------

class GameOver(TextGetter):
	def __init__(self, renderer, score):
		super().__init__(renderer, 'Thy name: ')
		self.title = hud.Text('GAME OVER', renderer, Constants.TITLE_FONT_SIZE, color=Colour.Burgundy)
		self.subtitle = hud.Text('Thy score: {}'.format(score), renderer, Constants.MENU_FONT_SIZE)

		self.title.position.y = int(20 * Constants._scale_ratio)
		self.title.centerHorizontally()
		self.subtitle.position.y = int(100 * Constants._scale_ratio)
		self.subtitle.centerHorizontally()

		self.score = score
	
	def handleEvent(self, e):
		super().handleEvent(e)
	
	def render(self, renderer):
		self.title.render(renderer)
		self.subtitle.render(renderer)
		super().render(renderer)
	
	def result(self):
		return (self.input, self.score)

	def typeOf(self):
		return 'GameOver'