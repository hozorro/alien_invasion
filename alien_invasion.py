#!/usr/bin/python3
#--coding:utf8--

import sys
import os
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from info_board import InfoBoard
import game_functions as gf
from pygame.sprite import Group

def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings=Settings()
	x=10
	y=25
	os.environ['SDL_VIDEO_WINDOW_POS']='%d,%d'%(x,y)
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')

	play_button=Button(ai_settings,screen,"Play")
	
	#创建一艘飞船
	ship=Ship(ai_settings,screen)
	stats=GameStats(ai_settings)
	bullets=Group()
	aliens=Group()
	gf.create_fleet(ai_settings,screen,ship,aliens)
	ib=InfoBoard(ai_settings,screen,stats)

	#开始游戏的主循环
	while True:
		gf.check_events(ai_settings,screen,stats,ib,play_button,ship,aliens,bullets)

		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,stats,ib,ship,aliens,bullets)
			gf.update_aliens(ai_settings,stats,ib,screen,ship,aliens,bullets)

		gf.update_screen(ai_settings,stats,ib,screen,ship,aliens,bullets,play_button)

run_game()
