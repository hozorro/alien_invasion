#!/usr/bin/python3
#--coding:utf8--

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""飞船类"""
	def __init__(self,ai_settings,screen):
		"""初始化飞船设置"""
		super(Ship,self).__init__()
		self.screen=screen
		self.ai_settings=ai_settings

		#加载飞船图像并获取其外接矩形
		self.image=pygame.image.load('images\ship.bmp')
		self.rect=self.image.get_rect()
		self.screen_rect=screen.get_rect()

		#设置飞船在屏幕中的初始位置
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom

		self.center=float(self.rect.centerx)

		#飞船移动标志
		self.moving_right=False
		self.moving_left=False

	def blitme(self):
		"""在制定位置绘制飞船"""
		self.screen.blit(self.image,self.rect)

	def update(self):
		"""根据移动标志调整飞船位置，用center存储浮点数的位置值"""
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.center+=self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left>0:
			self.center-=self.ai_settings.ship_speed_factor

		self.rect.centerx=self.center

	def center_ship(self):
		self.center=self.screen_rect.centerx