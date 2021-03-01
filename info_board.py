#!/usr/bin/python3
#--coding:utf8--

import pygame.font
from pygame.sprite import Group
from ship import Ship

class InfoBoard():
	"""游戏信息显示"""
	def __init__(self,ai_settings,screen,stats):
		self.screen=screen
		self.screen_rect=screen.get_rect()
		self.ai_settings=ai_settings
		self.stats=stats

		self.text_color=(90,190,90)
		self.font=pygame.font.SysFont(None,24)

		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		round_score=int(round(self.stats.score,-1))

		score_str='Score: '+'{:,}'.format(round_score)
		self.score_image=self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
		self.score_rect=self.score_image.get_rect()
		self.score_rect.right=self.screen_rect.right-20
		self.score_rect.top=10

	def prep_level(self):
		level_str='Level: '+str(self.stats.level)
		self.level_imgae=self.font.render(level_str,True,self.text_color,self.ai_settings.bg_color)
		self.level_rect=self.level_imgae.get_rect()
		self.level_rect.left=self.score_rect.left
		self.level_rect.top=self.score_rect.bottom+10

	def prep_high_score(self):
		round_high_score=int(round(self.stats.high_score,-1))
		high_score_str='High: '+'{:,}'.format(round_high_score)
		self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
		self.high_score_rect=self.high_score_image.get_rect()
		self.high_score_rect.centerx=self.screen_rect.centerx
		self.high_score_rect.top=10

	def prep_ships(self):
		self.ships=Group()
		for ship_num in range(self.stats.ships_left):
			ship=Ship(self.ai_settings,self.screen)
			ship.image=pygame.transform.scale(ship.image,(29,29))
			ship.rect=ship.image.get_rect()
			ship.rect.x=10+ship_num*ship.rect.width
			ship.rect.y=10
			self.ships.add(ship)


	def show_info(self):
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.level_imgae,self.level_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.ships.draw(self.screen)
