import pygame as pg
import settings
from settings import *
import enemys
from enemys import *
from player_stats import *



from tilemap import collide_hit_rect



def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def collide_with_event(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.collide_rect(sprite,group)
        if hits:



            sprite.map_change = True
            sprite.map_change_dest = group.destination
            # play_map_background = group.destination
            # sprite.vel.x = 0
            # sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.collide_rect(sprite,group)
        if hits:


            sprite.map_change = True
            sprite.map_change_dest = group.destination

            # play_map_background = group.destination
            # sprite.vel.y = 0
            # sprite.hit_rect.centery = sprite.pos.y


def collide_with_encounter(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.collide_rect(sprite,group)
        if hits:
            sprite.battle_loc = group.location
            sprite.battle = True
            enemys.enemy1 = group.enemy1
            enemys.enemy2 = group.enemy2
            enemys.enemy3 = group.enemy3
            enemys.enemy4 = group.enemy4
            enemys.enemy5 = group.enemy5
            #sprite.game.game_state = game_states['battle']




    if dir == 'y':
        hits = pg.sprite.collide_rect(sprite,group)
        if hits:
            sprite.battle_loc = group.location
            sprite.battle = True
            #sprite.game.game_state = game_states['battle']


def collide_with_dialog(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.collide_rect(sprite,group)
        if hits:
            sprite.dialog = True
            sprite.dialog_text1 = group.dialog1
            sprite.dialog_text2 = group.dialog2
            sprite.dialog_text3 = group.dialog3
            sprite.dialog_text4 = group.dialog4
            sprite.dialog_text5 = group.dialog5
            sprite.dialog_text6 = group.dialog6
            sprite.dialog_text7 = group.dialog7
            sprite.dialog_text8 = group.dialog8




    if dir == 'y':
        hits = pg.sprite.collide_rect(sprite,group)
        if hits:
            sprite.dialog = True
            sprite.dialog_text1 = group.dialog1
            sprite.dialog_text2 = group.dialog2
            sprite.dialog_text3 = group.dialog3
            sprite.dialog_text4 = group.dialog4
            sprite.dialog_text5 = group.dialog5
            sprite.dialog_text6 = group.dialog6
            sprite.dialog_text7 = group.dialog7
            sprite.dialog_text8 = group.dialog8




class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game



        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.frame = 1
        self.speed = PLAYER_SPEED
        self.player_img_1 = statemachine.GFX['female_front']
        self.player_img_2 = statemachine.GFX['female_front_l']
        self.player_img_3 = statemachine.GFX['female_front_r']
        self.player_img_4 = statemachine.GFX['female_back']
        self.player_img_5 = statemachine.GFX['female_back_l']
        self.player_img_6 = statemachine.GFX['female_back_r']
        self.player_img_7 = statemachine.GFX['female_right']
        self.player_img_8 = statemachine.GFX['female_right_l']
        self.player_img_9 = statemachine.GFX['female_right_r']
        self.player_img_10 = statemachine.GFX['female_left']
        self.player_img_11 = statemachine.GFX['female_left_l']
        self.player_img_12 = statemachine.GFX['female_left_r']

        self.image_dict_f = {1: self.player_img_1,
                             2: self.player_img_2,
                             3: self.player_img_3}

        self.image_dict_b = {1: self.player_img_4,
                             2: self.player_img_5,
                             3: self.player_img_6}

        self.image_dict_r = {1: self.player_img_7,
                             2: self.player_img_8,
                             3: self.player_img_9}
        self.image_dict_l = {1: self.player_img_10,
                             2: self.player_img_11,
                             3: self.player_img_12}

        self.image = self.image_dict_f[1]
        self.rect = self.image.get_rect().inflate(-5, -5)
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.select = False

        self.map_change = False
        self.map_change_dest = 0

        self.dialog = False
        self.dialog_text1 = None
        self.dialog_text2 = None
        self.dialog_text3 = None
        self.dialog_text4 = None
        self.dialog_text5 = None
        self.dialog_text6 = None
        self.dialog_text7 = None
        self.dialog_text8 = None
        self.dialog_time = 0
        self.dialog_time_after = 0
        self.info = False
        self.battle = False
        self.battle_loc = None

        self.time_since_last = 0
        self.time_count = 1

    def get_keys(self):
        self.vel = vec(0, 0)
        self.speed = PLAYER_SPEED



        keys = pg.key.get_pressed()
        if not self.dialog:
            if keys[pg.K_LSHIFT]:
                self.speed = PLAYER_SPEED * 2
                self.time_count *= 1.1
            if not keys[pg.K_LSHIFT]:
                self.time_count = 1.5
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.vel += vec(-self.speed,0)###########   chang to = for four dir  +=  for 8
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.vel += vec(self.speed,0)
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel += vec(0, -self.speed)
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel += vec(0, self.speed)
        if keys[pg.K_SPACE]:
            self.select = True
        else:
            self.select = False



    def animate(self):

        if self.time_since_last >= 20:
            if self.frame == 4:
                self.frame = 1
                ####down
            if self.vel == vec(0, self.speed):
                self.image = self.image_dict_f[self.frame]
                self.frame += 1
                ###up
            if self.vel == vec(0, -self.speed):
                self.image = self.image_dict_b[self.frame]
                self.frame += 1
                ####right
            if self.vel == vec(self.speed, 0):
                self.image = self.image_dict_r[self.frame]
                self.frame += 1
                ###left
            if self.vel == vec(-self.speed, 0):
                self.image = self.image_dict_l[self.frame]
                self.frame += 1
            else:
                pass
            self.time_since_last = 0
        else:
            self.time_since_last += self.time_count




    def update(self, dt):


        self.get_keys()
        self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')

        for event in self.game.event:
            collide_with_event(self, event, 'x')
            collide_with_event(self, event, 'y')
        for encounter in self.game.encounter:
            collide_with_encounter(self, encounter, 'x')
            collide_with_encounter(self, encounter, 'y')
        for dialog in self.game.dialog:
            if self.select:
                if self.dialog_time_after >= 10:
                    collide_with_dialog(self, dialog, 'x')
                    collide_with_dialog(self, dialog, 'y')
        if self.dialog:
            self.dialog_time += 1
            if self.dialog_time >= 10:
                if self.select:

                    self.dialog = False
                    self.dialog_time = 0
                    self.dialog_time_after = 0
                    self.info = True
            else:
                pass


        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')



        self.rect.center = self.hit_rect.center

        self.dialog_time_after += 1


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Event(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, destination):
        self.groups = game.event
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.destination = destination

class Encounter(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, location, enemy1, enemy2, enemy3, enemy4, enemy5):
        self.groups = game.encounter
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.location = location
        self.enemy1 = enemy1
        self.enemy2 = enemy2
        self.enemy3 = enemy3
        self.enemy4 = enemy4
        self.enemy5 = enemy5

class Dialog(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, dialog1, dialog2, dialog3, dialog4,
                 dialog5, dialog6, dialog7, dialog8):
        self.groups = game.dialog
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.dialog1 = dialog1
        self.dialog2 = dialog2
        self.dialog3 = dialog3
        self.dialog4 = dialog4
        self.dialog5 = dialog5
        self.dialog6 = dialog6
        self.dialog7 = dialog7
        self.dialog8 = dialog8