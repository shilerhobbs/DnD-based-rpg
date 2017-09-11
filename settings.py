import sys
import pygame as pg
import statemachine
import os




WIDTH = 480   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 320  # 16 * 48 or 32 * 24 or 64 * 12         480*320      1920*1280



vec = pg.math.Vector2


direction = {'up' : 0, 'down' : 1, 'left' : 2, 'right' : 3}

position = {'top_left' : 0, 'top_right' : 1, 'bottom_left' : 2, 'bottom_right' : 3,
            'left' : 4, 'right' : 5}



# Map List
map_dict = {'home_interior':'home_interior.tmx','home_exterior':'home_exterior.tmx',
            'cross_roads':'cross_roads.tmx','town_square':'town_square.tmx',
            'town_shop':'town_shop.tmx','town_house_1':'town_house_1.tmx',
            'town_house_2':'town_house_2.tmx','town_mayor_house':'town_mayor_house.tmx',
            'wild_field_1':'wild_field_1.tmx','wild_field_2':'wild_field_2.tmx',
            'dungeon_1_floor_1':'dungeon_1_floor_1.tmx','menu_test':'menu_test.tmx'}


background = ['Tile Layer 1','Tile Layer 2','Tile Layer 3']

forground = ['Tile Layer 4','Tile Layer 5','Tile Layer 6']
forground_1 = 'Tile Layer 4'




start_map = map_dict['home_interior']
back = map_dict['home_interior']
front = map_dict['home_interior']


play_map = start_map
play_map_background = back
play_map_forground = front




PLAYER_SPEED = .1


PLAYER_HIT_RECT = pg.Rect(0, 0, 24, 36)





