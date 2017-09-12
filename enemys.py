import sys
import pygame as pg
import statemachine
import settings
from os import path
from settings import *
import sprites
import tilemap
from player_stats import *






enemy1 = None
enemy2 = None
enemy3 = None
enemy4 = None
enemy5 = None




#####  bat stats
bat_img1 = statemachine.GFX['bat_left']
bat_img2 = statemachine.GFX['bat_left_l']
bat_img3 = statemachine.GFX['bat_left_r']

bat_stats = {'str' : 2, 'str mod' : -4, 'dex' : 15, 'dex mod' : 2, 'con' : 8, 'con mod' : -1,
                'int' : 2, 'int mod' : -4, 'wis' : 12, 'wis mod' : 1, 'cha' : 4, 'cha mod' : -3,
                'total_hit_points' : 3, 'current_hit_points' : 3,
                'speed' : 5, 'AC' : 12, 'atk_dam' : 1, 'atk_bonus' : 0,
             'img1' : bat_img1, 'img2' : bat_img2, 'img3' : bat_img3}




enemy_dict = {'bat' : bat_stats}







class Enemy(pg.sprite.Sprite):
    def __init__(self, game, dict):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.stats = dict
        self.img = self.stats['img_1']
        self.img1 = self.stats['img_1']
        self.img2 = self.stats['img_2']
        self.img3 = self.stats['img_3']