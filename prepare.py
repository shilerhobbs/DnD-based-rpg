"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg

import tools


SCREEN_SIZE = (800, 600)
WIDTH = SCREEN_SIZE[0]
HEIGHT = SCREEN_SIZE[1]
ORIGINAL_CAPTION = "Intro scene with movie"
vec = pg.math.Vector2

PLAYER_SPEED = 100
PLAYER_HIT_RECT = pg.Rect(0, 0, 24, 36)



map_dict = {'home_interior':'home_interior.tmx','home_exterior':'home_exterior.tmx',
            'cross_roads':'cross_roads.tmx','town_square':'town_square.tmx',
            'town_shop':'town_shop.tmx','town_house_1':'town_house_1.tmx',
            'town_house_2':'town_house_2.tmx','town_mayor_house':'town_mayor_house.tmx',
            'wild_field_1':'wild_field_1.tmx','wild_field_2':'wild_field_2.tmx',
            'dungeon_1_floor_1':'dungeon_1_floor_1.tmx','menu_test':'menu_test.tmx'}

play_map = map_dict['home_interior']



#Initialization
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


#Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
#MOV   = tools.load_all_movies(os.path.join("resources", "movies"))