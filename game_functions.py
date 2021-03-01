#!/usr/bin/python3
#--coding:utf8--

import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,stats,ib,ship,aliens,bullets):
	"""响应按键按下"""
	if event.key==pygame.K_RIGHT:
		#向右移动飞船
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		#向右移动飞船
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullets(ai_settings,screen,ship,bullets)
	elif event.key==pygame.K_p:
		start_game(ai_settings,screen,stats,ib,ship,aliens,bullets)
	elif event.key==pygame.K_q:
		sys.exit()

def check_keyup_events(event,ai_settings,screen,ship,bullets):
	"""响应按键松开"""
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

def check_events(ai_settings,screen,stats,ib,play_button,ship,aliens,bullets):
	#监视键盘和鼠标事件
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,ib,play_button,ship,aliens,bullets,mouse_x,mouse_y)
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,stats,ib,ship,aliens,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ai_settings,screen,ship,bullets)

def check_play_button(ai_settings,screen,stats,ib,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""检测是否点击了play按钮"""
	button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		start_game(ai_settings,screen,stats,ib,ship,aliens,bullets)

def start_game(ai_settings,screen,stats,ib,ship,aliens,bullets):
	ai_settings.initialize_dynamic_settings()
	pygame.mouse.set_visible(False)
	stats.reset_status()
	stats.game_active=True

	ib.prep_score()
	ib.prep_level()
	ib.prep_high_score()
	ib.prep_ships()

	aliens.empty()
	bullets.empty()

	create_fleet(ai_settings,screen,ship,aliens)
	ship.center_ship()

def update_screen(ai_settings,stats,ib,screen,ship,aliens,bullets,play_button):
	"""更新屏幕上的图像，并切换到新屏幕"""
	#每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)

	if stats.game_active:
		for bullet in bullets.sprites():
			bullet.draw_bullet()
		ship.blitme()
		#绘制外星人队列
		aliens.draw(screen)

		ib.show_info()
	else:
		play_button.draw_button()

	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings,screen,stats,ib,ship,aliens,bullets):
	"""更新子弹位置，并删除消失的子弹"""
	bullets.update()

	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)

	check_alien_bullet_collisions(ai_settings,screen,stats,ib,ship,aliens,bullets)

def check_alien_bullet_collisions(ai_settings,screen,stats,ib,ship,aliens,bullets):
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for c_aliens in collisions.values():
			stats.score+=ai_settings.alien_points*len(c_aliens)
			ib.prep_score()
		check_high_score(stats,ib)

	if len(aliens)==0:
		bullets.empty()
		ai_settings.increase_speed()

		stats.level+=1
		ib.prep_level()

		create_fleet(ai_settings,screen,ship,aliens)

def fire_bullets(ai_settings,screen,ship,bullets):
	"""发射子弹"""
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def get_aliens_number_x(ai_settings,alien_width):
	"""获取每行可容纳外星人的个数"""
	available_space_x=ai_settings.screen_width-2*alien_width
	num_aliens_x=int(available_space_x/(2*alien_width))
	return num_aliens_x

def get_alien_num_row(ai_settings,ship_height,alien_height):
	available_space_y=ai_settings.screen_height-ship_height-3*alien_height
	num_alien_rows=int(available_space_y/(2*alien_height))
	return num_alien_rows

def create_alien(ai_settings,screen,aliens,alien_num,row_num):
	"""创建外星人"""
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien_height=alien.rect.height
	alien.x=alien_width+alien_num*2*alien_width
	alien.rect.x=alien.x
	alien.y=alien_height+row_num*2*alien_height
	alien.rect.y=alien.y
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	"""创建外星人群"""
	alien=Alien(ai_settings,screen)
	num_aliens_x=get_aliens_number_x(ai_settings,alien.rect.width)
	num_rows=get_alien_num_row(ai_settings,ship.rect.height,alien.rect.height)

	for row_num in range(num_rows):
		for alien_num in range(num_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_num,row_num)

def check_fleet_edge(ai_settings,aliens):
	"""有外星人到达屏幕边缘时应采取的措施"""
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	"""改变外星人群移动的方向"""
	for alien in aliens.sprites():
		alien.y+=ai_settings.fleet_speed_drop
		alien.rect.y=alien.y
	ai_settings.fleet_direction*=-1

def update_aliens(ai_settings,stats,ib,screen,ship,aliens,bullets):
	"""更新外星人位置"""
	check_fleet_edge(ai_settings,aliens)
	aliens.update()

	#检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,ib,screen,ship,aliens,bullets)

	check_aliens_bottom(ai_settings,stats,ib,screen,ship,aliens,bullets)

def ship_hit(ai_settings,stats,ib,screen,ship,aliens,bullets):
	"""响应被外星人撞到飞船"""
	if stats.ships_left>1:
		stats.ships_left-=1
		ib.prep_ships()
		aliens.empty()
		bullets.empty()

		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		sleep(0.5)
	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,ib,screen,ship,aliens,bullets):
	"""检测外星人是否接触到屏幕底端"""
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			ship_hit(ai_settings,stats,ib,screen,ship,aliens,bullets)
			break

def check_high_score(stats,ib):
	if stats.score>stats.high_score:
		stats.high_score=stats.score
		ib.prep_high_score()