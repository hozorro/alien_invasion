#!/usr/bin/python3
#--coding:utf8--

import pygame
from pygame.sprite import Sprite

class Alien(Sprite ):
	"""外星人类"""
	def __init__(self,ai_settings,screen):
		super(Alien,self).__init__()
		self.ai_settings=ai_settings
		self.screen=screen

		self.image=pygame.image.load('images\\alien.bmp')
		self.rect=self.image.get_rect()

		self.rect.x=self.rect.width
		self.rect.y=self.rect.height

		self.x=float(self.rect.x)
		self.y=float(self.rect.y)

	def blitme(self):
		self.screen.blit(self.image,self.rect)

	def update(self):
		self.x+=self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction
		self.rect.x=self.x

	def check_edge(self):
		screen_rect=self.screen.get_rect()
		if self.rect.right>=screen_rect.right or self.rect.left<=0:
			return True