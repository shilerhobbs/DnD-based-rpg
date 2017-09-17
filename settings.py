import sys
import pygame as pg
import statemachine
import os

WIDTH = 480   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 320  # 16 * 48 or 32 * 24 or 64 * 12         480*320      1920*1280

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))






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
play_map_for = front




PLAYER_SPEED = .1


PLAYER_HIT_RECT = pg.Rect(0, 0, 24, 36)




### Resource loading functions.
def load_all_gfx(directory,colorkey=(255,0,255),accept=(".png",".jpg",".bmp")):
    """Load all graphics with extensions in the accept argument.  If alpha
    transparency is found in the image the image will be converted using
    convert_alpha().  If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey."""
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """Create a dictionary of paths to music files in given directory
    if their extensions are in accept."""
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=(".ttf",)):
    """Create a dictionary of paths to font files in given directory
    if their extensions are in accept."""
    return load_all_music(directory, accept)


def load_all_movies(directory, accept=(".mpg",)):
    """Create a dictionary of paths to movie files in given directory
    if their extensions are in accept."""
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """Load all sfx of extensions found in accept.  Unfortunately it is
    common to need to set sfx volume on a one-by-one basis.  This must be done
    manually if necessary in the setup module."""
    effects = {}
    for fx in os.listdir(directory):
        name,ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects


def strip_from_sheet(sheet, start, size, columns, rows=1):
    """Strips individual frames from a sprite sheet given a start location,
    sprite size, and number of columns and rows."""
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames


def strip_coords_from_sheet(sheet, coords, size):
    """Strip specific coordinates from a sprite sheet."""
    frames = []
    for coord in coords:
        location = (coord[0]*size[0], coord[1]*size[1])
        frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames


def get_cell_coordinates(rect, point, size):
    """Find the cell of size, within rect, that point occupies."""
    cell = [None, None]
    point = (point[0]-rect.x, point[1]-rect.y)
    cell[0] = (point[0]//size[0])*size[0]
    cell[1] = (point[1]//size[1])*size[1]
    return tuple(cell)


def cursor_from_image(image):
    """Take a valid image and create a mouse cursor."""
    colors = {(0,0,0,255) : "X",
              (255,255,255,255) : "."}
    rect = image.get_rect()
    icon_string = []
    for j in range(rect.height):
        this_row = []
        for i in range(rect.width):
            pixel = tuple(image.get_at((i,j)))
            this_row.append(colors.get(pixel, " "))
        icon_string.append("".join(this_row))
    return icon_string

