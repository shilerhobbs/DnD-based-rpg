import sys
import pygame as pg
import pickle
import statemachine
import settings
from os import path
from settings import *
import sprites
import tilemap
from player_stats import *
from random import randint
import enemys
from enemys import *
from numpy import subtract as sub
import collections


######  debug
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


class SplashScreen(statemachine.GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.direction = None
        self.position = settings.position['top_left']
        self.select = False
        self.back_ground = statemachine.GFX['Menu_background']
        self.button_tl = statemachine.GFX['Start_button']
        self.button_tl_loc = (22, 175)
        self.button_tr = statemachine.GFX['Continue_button']
        self.button_tr_loc = (251, 175)
        self.button_bl = statemachine.GFX['Credits_button']
        self.button_bl_loc = (22, 248)
        self.button_br = statemachine.GFX['Quit_button']
        self.button_br_loc = (251, 248)
        self.cursor = statemachine.GFX['Cursor']
        self.cursor_loc = (22, 189)
        self.cursor_pos_tl = (22, 189)
        self.cursor_pos_tr = (251, 189)
        self.cursor_pos_bl = (22, 262)
        self.cursor_pos_br = (251, 262)
        self.next_state = "STAT_F"

    def update(self, dt):

        if self.select:
            if self.position == settings.position['top_left']:
                self.persist['player_stats'] = player_stats
                self.next_state = "STAT_F"
                self.done  = True

            if self.position == settings.position['top_right']:
                self.next_state = "GAMEPLAY"
                self.load_game()
                self.done =True

            if self.position == settings.position['bottom_right']:
                self.quit = True
            else:
                pass

        if self.direction == settings.direction['left']:
            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            else:
                pass

        if self.direction == settings.direction['right']:
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass

        if self.direction == settings.direction['up']:
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            else:
                pass

        if self.direction == settings.direction['down']:
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass


        else:
            pass

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.direction = settings.direction['left']
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.direction = settings.direction['right']
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.direction = settings.direction['up']
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.direction = settings.direction['down']
            if keys[pg.K_SPACE]:
                self.select = True
            else:
                self.select = False


    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.back_ground,(0,0))
        surface.blit(self.button_tl,self.button_tl_loc)
        surface.blit(self.button_tr, self.button_tr_loc)
        surface.blit(self.button_bl, self.button_bl_loc)
        surface.blit(self.button_br, self.button_br_loc)
        surface.blit(self.cursor, self.cursor_loc)



class Gameplay(statemachine.GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.event = pg.sprite.Group()
        self.encounter = pg.sprite.Group()
        self.dialog = pg.sprite.Group()
        self.pause = False
        self.persist['current_map'] = settings.start_map
        self.level_screen = False
        # self.player = sprites.Player(self, 0, 0)
        self.encounter_timer = 0
        self.rand_enemy1 = None
        self.rand_enemy2 = None
        self.rand_enemy3 = None
        self.rand_enemy4 = None
        self.rand_enemy5 = None
        self.rand_battle = None
        self.player_step = False

    def make_map(self):
        for sprite in self.all_sprites:
            self.all_sprites.remove(sprite)
        for wall in self.walls:
            self.walls.remove(wall)
        for event in self.event:
            self.event.remove(event)
        for dialog in self.dialog:
            self.dialog.remove(dialog)
        for encounter in self.encounter:
            self.encounter.remove(encounter)
        self.map = tilemap.TiledMap(path.join('resources','maps', settings.play_map))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()

        # self.map_img_forgound.rect = self.map_img_forgound.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = sprites.Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                sprites.Obstacle(self, tile_object.x, tile_object.y,
                                 tile_object.width, tile_object.height)

            if tile_object.name == 'event':
                sprites.Event(self, tile_object.x, tile_object.y,
                              tile_object.width, tile_object.height,
                              tile_object.properties['destination'])

            if tile_object.name == 'encounter':
                sprites.Encounter(self, tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height,
                                  tile_object.properties['location'],
                                  tile_object.properties['enemy1'],
                                  tile_object.properties['enemy2'],
                                  tile_object.properties['enemy3'],
                                  tile_object.properties['enemy4'],
                                  tile_object.properties['enemy5'])

            if tile_object.name == 'dialog':
                sprites.Dialog(self, tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height,
                                  tile_object.properties['dialog1'],
                               tile_object.properties['dialog2'],
                               tile_object.properties['dialog3'],
                               tile_object.properties['dialog4'],
                               tile_object.properties['dialog5'],
                               tile_object.properties['dialog6'],
                               tile_object.properties['dialog7'],
                               tile_object.properties['dialog8'])

        self.camera = tilemap.Camera(self.map.width, self.map.height)

        self.encounters = self.map.encounters


    def dialog_box(self, text1, text2, text3, text4, text5, text6, text7, text8):
        self.dialog_font = pg.font.Font('A Love of Thunder.ttf',16)
        self.dialog_box_img = statemachine.GFX['Dialog_background']
        self.dialog_box_loc = (110,24)
        self.dialog_text1 = text1
        self.dialog_text2 = text2
        self.dialog_text3 = text3
        self.dialog_text4 = text4
        self.dialog_text5 = text5
        self.dialog_text6 = text6
        self.dialog_text7 = text7
        self.dialog_text8 = text8
        self.dialog1_text_loc = (120, 28)
        self.dialog2_text_loc = (120, 46)
        self.dialog3_text_loc = (120, 64)
        self.dialog4_text_loc = (120, 82)
        self.dialog5_text_loc = (120, 100)
        self.dialog6_text_loc = (120, 116)
        self.dialog7_text_loc = (120, 134)
        self.dialog8_text_loc = (120, 152)


    def encouter_gen(self):
        p = player_stats['level']
        r = randint(1, 10)
        self.rand_enemy_list = encounter_dict[p][r]

        self.rand_enemy1 = self.rand_enemy_list[0]
        self.rand_enemy2 = self.rand_enemy_list[1]
        self.rand_enemy3 = self.rand_enemy_list[2]
        self.rand_enemy4 = self.rand_enemy_list[3]
        self.rand_enemy5 = self.rand_enemy_list[4]
        enemys.enemy1 = self.rand_enemy1
        enemys.enemy2 = self.rand_enemy2
        enemys.enemy3 = self.rand_enemy3
        enemys.enemy4 = self.rand_enemy4
        enemys.enemy5 = self.rand_enemy5


    def startup(self, persistent):

        self.rand_enemy1 = None
        self.rand_enemy2 = None
        self.rand_enemy3 = None
        self.rand_enemy4 = None
        self.rand_enemy5 = None
        self.rand_battle = None
        self.player_step = False

        self.persist = persistent
        if 'current_map' in self.persist:
            settings.play_map = self.persist['current_map']
        self.make_map()
        self.info1 = 'wasd to move'
        self.info2 = 'space to interact'
        self.dialog_box(self.info1,self.info2,None,None,None,None,None,None)
        self.pause = False
        if not 'intro_seen' in self.persist:
            self.player.dialog_text1 = self.info1
            self.player.dialog_text2 = self.info2
            self.player.dialog = True
            self.persist['intro_seen'] = True

        self.encounter_timer = 0





    def get_event(self, event):

        if self.encounters:

            if self.player.player_step:
                self.encounter_timer += 1

            if self.encounter_timer >= 10:
                self.player.battle = True
                self.encouter_gen()
                self.rand_battle = sprites.Encounter(self, 1, 1, 10, 10,
                                                     self.player.pos,
                                                     self.rand_enemy1,
                                                     self.rand_enemy2,
                                                     self.rand_enemy3,
                                                     self.rand_enemy4,
                                                     self.rand_enemy5)
                self.encounter_timer = 0


        if event.type == pg.QUIT:
            self.quit = True
        if self.player.dialog:
            self.dialog_box(self.player.dialog_text1, self.player.dialog_text2, self.player.dialog_text3,
                            self.player.dialog_text4, self.player.dialog_text5, self.player.dialog_text6,
                            self.player.dialog_text7, self.player.dialog_text8)
        if not self.player.dialog:
            self.player.get_keys()
        if self.player.map_change:
            self.persist['current_map'] = map_dict[self.player.map_change_dest]
            settings.play_map = self.persist['current_map']

            self.make_map()
        if self.player.battle:
            self.next_state = "BATTLE"
            self.done = True
        if self.player.pause:
            self.next_state = "PAUSE"
            self.done = True


    def level_up(self):
        self.persist['player_stats']['level'] += 1
        self.persist['player_stats']['prof_points'] += 2
        self.persist['player_stats']['total_hit_points'] += randint(self.persist['player_stats']['hit_die_low'],
                                                                    self.persist['player_stats']['hit_die_high']) + self.persist['player_stats']['con mod']
        if self.persist['player_stats']['level'] % 2 == 0:
            self.persist['player_stats']['atr_points'] += 1
        self.level_screen = True



    def update(self, dt):
        self.player.update(dt)
        self.camera.update(self.player)
        ###  LEVEL UP
        if player_stats['exp'] >= 300:
            self.level_up()
            if player_stats['exp'] >= 900:
                self.level_up()
                if player_stats['exp'] >= 2700:
                    self.level_up()
                    if player_stats['exp'] >= 6500:
                        self.level_up()
                        if player_stats['exp'] >= 14000:
                            self.level_up()
                            if player_stats['exp'] >= 23000:
                                self.level_up()
                                if player_stats['exp'] >= 34000:
                                    self.level_up()
                                    if player_stats['exp'] >= 48000:
                                        self.level_up()
                                        if player_stats['exp'] >= 64000:
                                            self.level_up()
                                            if player_stats['exp'] >= 85000:
                                                self.level_up()
                                                if player_stats['exp'] >= 100000:
                                                    self.level_up()
                                                    if player_stats['exp'] >= 120000:
                                                        self.level_up()
                                                        if player_stats['exp'] >= 140000:
                                                            self.level_up()
                                                            if player_stats['exp'] >= 165000:
                                                                self.level_up()

    def draw(self, surface):
        surface.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            surface.blit(sprite.image, self.camera.apply(sprite))


        for sprite in self.all_sprites:
            pg.draw.rect(surface, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        for wall in self.walls:
            pg.draw.rect(surface, ORANGE, self.camera.apply_rect(wall.rect), 1)
        for event in self.event:
            pg.draw.rect(surface, CYAN, self.camera.apply_rect(event.rect), 1)
        for dialog in self.dialog:
            pg.draw.rect(surface, RED, self.camera.apply_rect(dialog.rect), 1)
        for encounter in self.encounter:
            pg.draw.rect(surface, RED, self.camera.apply_rect(encounter.rect), 1)
        ############


        if self.player.dialog:
            surface.blit(self.dialog_box_img,self.dialog_box_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text1, False, BLACK, None),
                         self.dialog1_text_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text2, True, BLACK),
                         self.dialog2_text_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text3, True, BLACK),
                         self.dialog3_text_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text4, True, BLACK),
                         self.dialog4_text_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text5, True, BLACK),
                         self.dialog5_text_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text6, True, BLACK),
                         self.dialog6_text_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text7, True, BLACK),
                         self.dialog7_text_loc)
            surface.blit(self.dialog_font.render(self.player.dialog_text8, True, BLACK),
                         self.dialog8_text_loc)



class BattleScreen(statemachine.GameState):
    def __init__(self):
        super(BattleScreen, self).__init__()
        self.party = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.direction = None
        self.position = settings.position['top_left']
        self.select = False
        self.button_tl = statemachine.GFX['Attack_button']
        self.button_tl_loc = (4,268)
        self.button_tr = statemachine.GFX['Item_button']
        self.button_tr_loc = (122,268)
        self.button_bl = statemachine.GFX['Equip_button']
        self.button_bl_loc = (4,294)
        self.button_br = statemachine.GFX['Flee_button']
        self.button_br_loc = (122,294)
        self.cursor = statemachine.GFX['small_Cursor']
        self.cursor_down = statemachine.GFX['small_Cursor_down']

        self.cursor_loc = (-2,269)





        self.cursor_pos_tl = (-2, 269)
        self.cursor_pos_tr = (121, 269)
        self.cursor_pos_bl = (-2, 295)
        self.cursor_pos_br = (121, 295)
        self.layer_1 = statemachine.GFX['Mountains_battleback']
        self.layer_2 = statemachine.GFX['Battle_menu_back']
        self.layer_2_loc = (0, 264)
        self.player_img = statemachine.GFX['female_right']
        self.player_img_1 = statemachine.GFX['female_right']
        self.player_img_2 = statemachine.GFX['female_right_l']
        self.player_img_3 = statemachine.GFX['female_right_r']
        self.player_loc = (162, 193)
        self.time_since_last = 0
        self.frame = 1


        self.enemy1 = None
        self.enemy2 = None
        self.enemy3 = None
        self.enemy4 = None
        self.enemy5 = None

        self.part1 = None
        self.party1_loc = (162, 193)
        self.party2 = None
        self.party2_loc = (82, 193)
        self.party3 = None
        self.party3_loc = (122, 193)

        self.enemy_list = [self.enemy1, self.enemy2, self.enemy3,
                            self.enemy4, self.enemy5]

        self.enemy1_loc = (247, 215)
        self.enemy2_loc = (295, 206)
        self.enemy3_loc = (343, 215)
        self.enemy4_loc = (391, 206)
        self.enemy5_loc = (439, 215)
        self.enemy_locs = [self.enemy1_loc, self.enemy2_loc, self.enemy3_loc,
                           self.enemy4_loc, self.enemy5_loc]

        self.cursor_down_loc = (252, 192)
        self.target_pos = {'first': 1, 'second': 2, 'third': 3,
                           'fourth': 4, 'fifth': 5}






        self.enemy1_cur_loc = (252, 180)
        self.enemy2_cur_loc = (300, 170)
        self.enemy3_cur_loc = (348, 180)
        self.enemy4_cur_loc = (396, 170)
        self.enemy5_cur_loc = (444, 180)
        self.enemy_cur_locs = [self.enemy1_cur_loc, self.enemy2_cur_loc, self.enemy3_cur_loc,
                               self.enemy4_cur_loc, self.enemy5_cur_loc]

        self.cursor_down_pos = self.target_pos['first']



        self.next_state = "GAMEPLAY"

        self.x = 0
        self.s = 0




        self.attack = False
        self.target = False
        self.melee = False
        self.battle_finish = False
        self.exp_earned = 0

        self.damage_done = False
        self.damage_amount = 0
        self.damage_loc = None
        self.damage_timer = 0

        self.miss = False
        self.miss_timer = 0
        self.miss_loc = None

        self.turn_count = 0
        self.turns = []
        self.turns_order = []
        self.player_turn = False
        self.current_sprite = None


    def startup(self, persistent):
        self.select = False
        self.attack = False
        self.target = False
        self.melee = False
        self.battle_finish = False
        self.damage_done = False
        self.damage_amount = 0
        self.damage_loc = None
        self.exp_earned = 0
        self.damage_timer = 0
        self.miss = False
        self.miss_loc = None
        self.miss_timer = 0
        self.turn_count = 0
        self.turns = []
        self.enemy1 = enemys.enemy1
        self.enemy2 = enemys.enemy2
        self.enemy3 = enemys.enemy3
        self.enemy4 = enemys.enemy4
        self.enemy5 = enemys.enemy5
        self.enemy_list = [self.enemy1, self.enemy2, self.enemy3,
                           self.enemy4, self.enemy5]
        self.party1 = player_stats['party']['party3']
        self.party2 = player_stats['party']['party2']
        self.party3 = player_stats['party']['party3']
        self.party1_init = 0
        self.party2_init = 0
        self.party3_init = 0
        self.enemy1_init = 0
        self.enemy2_init = 0
        self.enemy3_init = 0
        self.enemy4_init = 0
        self.enemy5_init = 0
        self.x = 0
        self.t = 0
        self.init_list = {}
        if not player_stats['party']['party1'] == None:
            self.party1 = Player_bat(self, player_stats, self.party1_loc)

        if not player_stats['party']['party2'] == None:
            self.party2 = Player_bat(self, player_stats['party2_stats'], self.party2_loc)

        if not player_stats['party']['party3'] == None:
            self.party3 = Player_bat(self, player_stats['party3_stats'], self.party3_loc)

        if not self.enemy1 == '':
            self.enemy1 = enemys.Enemy(self, enemys.enemy_dict[self.enemy1], self.enemy_locs[0])


        else:
            self.enemy1 = None
        if not self.enemy2 == '':
            self.enemy2 = enemys.Enemy(self, enemys.enemy_dict[self.enemy2], self.enemy_locs[1])

        else:
            self.enemy2 = None
        if not self.enemy3 == '':
            self.enemy3 = enemys.Enemy(self, enemys.enemy_dict[self.enemy3], self.enemy_locs[2])

        else:
            self.enemy3 = None
        if not self.enemy4== '':
            self.enemy4 = enemys.Enemy(self, enemys.enemy_dict[self.enemy4], self.enemy_locs[3])

        else:
            self.enemy4 = None
        if not self.enemy5 == '':
            self.enemy5 = enemys.Enemy(self, enemys.enemy_dict[self.enemy5], self.enemy_locs[4])

        else:
            self.enemy5 = None
        self.turns_order = []

        for enemy in self.enemy:
            enemy.init_roll()
            self.init_list[enemy.init] = self
            self.all_sprites.add(enemy)
            self.t += 1
            print('enemy', enemy, vars(enemy))
        for party in self.party:
            party.init_roll()
            self.init_list[party.init] = self
            self.all_sprites.add(party)
            self.t += 1


        # self.turns = collections.OrderedDict(sorted(self.init_list.items(), reverse=True))

        for key in self.init_list.keys():
            self.turns_order.append(key)

        self.turns_order.sort(reverse=True)

        for i in range(len(self.turns_order)):
            self.turns.append(self.init_list[self.turns_order[i]])

        self.turn_count = 0

        self.enemy_list = (self.enemy1, self.enemy2, self.enemy3,
                           self.enemy4, self.enemy5)
        print('self.turns',self.turns)
        self.turn_count_len = len(self.turns_order)



        self.turns[self.turn_count].turn = True

        print(self.turns)
        print(self.turns_order)
        print(self.init_list)
        print(self.turns[self.turn_count])
        print(vars(self.turns[self.turn_count]))

        for sprite in self.all_sprites:
            if sprite.init == self.turns_order[0]:
                sprite.turn = True



        #self.start_fight(enemys.enemy1,enemys.enemy2,enemys.enemy3,enemys.enemy4,enemys.enemy5)


    def animate(self):

        if self.time_since_last >= 10:

            if self.frame == 5:
                self.frame = 1

            elif self.frame == 1:
                for enemy in self.enemy:
                    enemy.img = enemy.img1
                for party in self.party:
                    party.img = party.img1
                self.frame += 1

            elif self.frame == 2:
                for enemy in self.enemy:
                    enemy.img = enemy.img2
                for party in self.party:
                    party.img = party.img2
                self.frame += 1
            elif self.frame == 3:
                for enemy in self.enemy:
                    enemy.img = enemy.img1
                for party in self.party:
                    party.img = party.img1
                self.frame += 1
            elif self.frame == 4:
                for enemy in self.enemy:
                    enemy.img = enemy.img3
                for party in self.party:
                    party.img = party.img3
                self.frame += 1
            else:
                pass
            self.time_since_last = 0

        else:
            self.time_since_last += 1

    def update(self, dt):
        print(self.all_sprites)

        # Turn counter
        for sprite in self.all_sprites:
            print(sprite, sprite.turn)
            if sprite.done:
                sprite.done = False
                sprite.turn = False
                self.turn_count += 1
                if self.turn_count > self.turn_count_len:
                    self.turn_count = 1
                if sprite.player:
                    self.player_turn = False

                ##CONFIRM CHANGE
                for spri in self.all_sprites:
                    if spri.init == self.turns_order[self.turn_count - 1]:
                        spri.turn = True
                    else:
                        pass

                ##




            if sprite.turn:
                if sprite.player:
                    self.player_turn = True
                    self.current_sprite = sprite
                else:
                    sprite.take_turn()

        if not self.party1 == None:
            pass



        # finish if all enemys are dead
        if self.enemy1 == None:
            if self.enemy2 == None:
                if self.enemy3 == None:
                    if self.enemy4 == None:
                        if self.enemy5 == None:
                            self.battle_finish = True
        else:
            pass

        if self.s == 5:
            self.s = 0
        if self.s == -1:
            self.s = 4


        # kill enemyies with 0 health
        for enemy in self.enemy:

            if enemy.health <= 0:
                self.exp_earned += enemy.stats['exp']
                enemy.kill()
            if enemy.turn:
                enemy.take_turn()
        if not self.enemy1 == None:
            if not self.enemy1.alive():
                self.enemy1 = None
        if not self.enemy2 == None:
            if not self.enemy2.alive():
                self.enemy2 = None
        if not self.enemy3 == None:
            if not self.enemy3.alive():
                self.enemy3 = None
        if not self.enemy4 == None:
            if not self.enemy4.alive():
                self.enemy4 = None
        if not self.enemy5 == None:
            if not self.enemy5.alive():
                self.enemy5 = None

        self.animate()

        if not self.attack:
            self.button_tl = statemachine.GFX['Attack_button']
            self.button_tr = statemachine.GFX['Item_button']
            self.button_bl = statemachine.GFX['Equip_button']
            self.button_br = statemachine.GFX['Flee_button']
        if self.attack:
            self.button_tl = statemachine.GFX['Melee_button']
            self.button_tr = statemachine.GFX['Ranged_button']
            self.button_bl = statemachine.GFX['Magic_button']
            self.button_br = statemachine.GFX['Back_button']

        if self.player_turn:

            if self.select:
                if self.battle_finish:

                    for enemy in self.enemy:
                        enemy.kill()
                    for party in self.party:
                        party.kill()

                    player_stats['exp'] += self.exp_earned
                    self.done = True

                #first enemy
                if self.target:
                    if self.cursor_down_loc == self.enemy1_cur_loc:
                        if not self.enemy1:
                            print('no target')
                        else:
                            self.attack = False
                            self.melee = False
                            self.target = False
                            self.current_sprite.attack(self.enemy1)
                    if self.cursor_down_loc == self.enemy2_cur_loc:
                        if not self.enemy2:
                            print('no target')
                        else:
                            self.attack = False
                            self.melee = False
                            self.target = False
                            self.current_sprite.attack(self.enemy2)
                    if self.cursor_down_loc == self.enemy3_cur_loc:
                        if not self.enemy3:
                            print('no target')
                        else:
                            self.attack = False
                            self.melee = False
                            self.target = False
                            self.current_sprite.attack(self.enemy3)
                    if self.cursor_down_loc == self.enemy4_cur_loc:
                        if not self.enemy4:
                            print('no target')
                        else:
                            self.attack = False
                            self.melee = False
                            self.target = False
                            self.current_sprite.attack(self.enemy4)
                    if self.cursor_down_loc == self.enemy5_cur_loc:
                        if not self.enemy5:
                            print('no target')
                        else:
                            self.attack = False
                            self.melee = False
                            self.target = False
                            self.current_sprite.attack(self.enemy5)

                ###   ATTACK
                if self.position == settings.position['top_left']:
                    if self.attack:
                        self.melee = True
                        self.select = False
                    if not self.attack:
                        self.attack = True
                        self.select = False

                ###   ITEM
                if self.position == settings.position['top_right']:
                    pass
                ###   EQUIP
                if self.position == settings.position['bottom_left']:
                    pass
                ###   FLEE
                if self.position == settings.position['bottom_right']:
                    if not self.attack:
                        flee_chance = randint(1, 20)
                        if flee_chance >= 4:
                            self.battle_finish = True
                        else:
                            pass
                    if self.attack:
                        self.attack = False
                        self.select = False


        if self.direction == settings.direction['left']:
            if self.target:
                self.cursor_down_loc = self.enemy_cur_locs[self.s]
                self.s -= 1

            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            else:
                pass
            self.direction = None

        if self.direction == settings.direction['right']:
            if self.target:
                self.cursor_down_loc = self.enemy_cur_locs[self.s]
                self.s += 1
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass
            self.direction = None

        if self.direction == settings.direction['up']:
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            else:
                pass
            self.direction = None

        if self.direction == settings.direction['down']:
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass
            self.direction = None

        if self.melee:
            self.target = True






    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.direction = settings.direction['left']
                # self.s -= 1
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.direction = settings.direction['right']
                # self.s += 1
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.direction = settings.direction['up']
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.direction = settings.direction['down']
            if keys[pg.K_SPACE]:
                self.select = True
            else:
                self.select = False

    def dialog_box(self, text1, text2, text3, text4, text5, text6, text7, text8):
        self.dialog_font = pg.font.Font('A Love of Thunder.ttf',16)
        self.dialog_box_img = statemachine.GFX['Dialog_background']
        self.dialog_box_loc = (110,24)
        self.dialog_text1 = text1
        self.dialog_text2 = text2
        self.dialog_text3 = text3
        self.dialog_text4 = text4
        self.dialog_text5 = text5
        self.dialog_text6 = text6
        self.dialog_text7 = text7
        self.dialog_text8 = text8
        self.dialog1_text_loc = (120, 28)
        self.dialog2_text_loc = (120, 46)
        self.dialog3_text_loc = (120, 64)
        self.dialog4_text_loc = (120, 82)
        self.dialog5_text_loc = (120, 100)
        self.dialog6_text_loc = (120, 116)
        self.dialog7_text_loc = (120, 134)
        self.dialog8_text_loc = (120, 152)

    def text_sccreen(self):
        self.dialog_font = pg.font.Font('A Love of Thunder.ttf',24)



    def draw(self, surface):

        surface.fill(pg.Color("black"))
        surface.blit(self.layer_1,(0,0))
        surface.blit(self.layer_2,self.layer_2_loc)
        surface.blit(self.button_tl,self.button_tl_loc)
        surface.blit(self.button_tr, self.button_tr_loc)
        surface.blit(self.button_bl, self.button_bl_loc)
        surface.blit(self.button_br, self.button_br_loc)
        if self.target:
            surface.blit(self.cursor_down, self.cursor_down_loc)

        for enemy in self.enemy:

            surface.blit(enemy.img, enemy.loc)
        for party in self.party:
            surface.blit(party.img, party.loc)
        if not self.target:
            if not self.battle_finish:
                if self.player_turn:
                    surface.blit(self.cursor, self.cursor_loc)

        if self.battle_finish:
            self.dialog_box(str(self.exp_earned), None, None, None, None, None, None, None)
            surface.blit(self.dialog_box_img,self.dialog_box_loc)
            surface.blit(self.dialog_font.render(self.dialog_text1, False, BLACK, None),
                         self.dialog1_text_loc)
            surface.blit(self.dialog_font.render(self.dialog_text2, True, BLACK),
                         self.dialog2_text_loc)
            surface.blit(self.dialog_font.render(self.dialog_text3, True, BLACK),
                         self.dialog3_text_loc)
            surface.blit(self.dialog_font.render(self.dialog_text4, True, BLACK),
                         self.dialog4_text_loc)
            surface.blit(self.dialog_font.render(self.dialog_text5, True, BLACK),
                         self.dialog5_text_loc)
            surface.blit(self.dialog_font.render(self.dialog_text6, True, BLACK),
                         self.dialog6_text_loc)
            surface.blit(self.dialog_font.render(self.dialog_text7, True, BLACK),
                         self.dialog7_text_loc)
            surface.blit(self.dialog_font.render(self.dialog_text8, True, BLACK),
                         self.dialog8_text_loc)
        if self.damage_done:
            if self.damage_timer >= 100:
                self.damage_done = False
                self.damage_timer = 0
            self.text_sccreen()
            surface.blit(self.dialog_font.render((str(self.damage_amount)), False, RED),
                                                 self.damage_loc)
            self.damage_loc = tuple(sub(self.damage_loc, (0, 1)))
            self.damage_timer += 1


        if self.miss:
            if self.miss_timer >= 100:
                self.miss = False
                self.miss_timer = 0
            self.text_sccreen()
            surface.blit(self.dialog_font.render('Miss', False, BLUE),
                         self.miss_loc)
            self.miss_loc = tuple(sub(self.miss_loc, (0, 1)))
            self.miss_timer += 1


    def player_melee_attack(self, target):
        atk_roll = randint(1, 20) + self.persist['player_stats']['str mod']
        if atk_roll >= target.stats['AC']:
            dam_roll = randint(self.persist['player_stats']['melee_dam_low'], self.persist['player_stats']['melee_dam_high'])
            target.health -= dam_roll
            print('hit for', dam_roll, 'damage')
        else:
            print('miss / block')


class PauseScreen(statemachine.GameState):
    def __init__(self):
        super(PauseScreen, self).__init__()
        self.direction = None
        self.position = settings.position['top_left']
        self.select = False
        self.back_ground = statemachine.GFX['Menu_background']
        self.button_tl = statemachine.GFX['Start_button']
        self.button_tl_loc = (22, 175)
        self.button_tr = statemachine.GFX['Continue_button']
        self.button_tr_loc = (251, 175)
        self.button_bl = statemachine.GFX['Credits_button']
        self.button_bl_loc = (22, 248)
        self.button_br = statemachine.GFX['Quit_button']
        self.button_br_loc = (251, 248)
        self.cursor = statemachine.GFX['Cursor']
        self.cursor_loc = (22, 189)
        self.cursor_pos_tl = (22, 189)
        self.cursor_pos_tr = (251, 189)
        self.cursor_pos_bl = (22, 262)
        self.cursor_pos_br = (251, 262)
        self.save_text = statemachine.GFX['Saved_text']
        self.save_text_loc = (34, 34)

        self.next_state = "GAMEPLAY"
        self.saved = False
        self.t = 0

    def update(self, dt):

        if self.saved:
            if self.t >= 100:
                self.t = 0
                self.saved = False
            self.t += 1

        if self.select:
            if self.position == settings.position['top_left']:
                self.next_state = "GAMEPLAY"
                self.select = False
                self.done  = True
            if self.position == settings.position['top_right']:
                self.save_game()
                self.saved = True


            if self.position == settings.position['bottom_right']:
                self.quit = True
            else:
                pass

        if self.direction == settings.direction['left']:
            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            else:
                pass

        if self.direction == settings.direction['right']:
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass

        if self.direction == settings.direction['up']:
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            else:
                pass

        if self.direction == settings.direction['down']:
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass


        else:
            pass

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.direction = settings.direction['left']
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.direction = settings.direction['right']
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.direction = settings.direction['up']
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.direction = settings.direction['down']
            if keys[pg.K_SPACE]:
                self.select = True
            else:
                self.select = False


    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.back_ground,(0,0))
        surface.blit(self.button_tl,self.button_tl_loc)
        surface.blit(self.button_tr, self.button_tr_loc)
        surface.blit(self.button_bl, self.button_bl_loc)
        surface.blit(self.button_br, self.button_br_loc)
        surface.blit(self.cursor, self.cursor_loc)
        if self.saved:
            surface.blit(self.save_text, self.save_text_loc)




class StatScreen(statemachine.GameState):
    def __init__(self):
        super(StatScreen, self).__init__()
        self.direction = None
        self.position = settings.position['top_left']
        self.select = False
        self.back_ground = statemachine.GFX['Menu_background']
        self.button_tl = statemachine.GFX['Start_button']
        self.button_tl_loc = (22, 175)
        self.button_tr = statemachine.GFX['Continue_button']
        self.button_tr_loc = (251, 175)
        self.button_bl = statemachine.GFX['Credits_button']
        self.button_bl_loc = (22, 248)
        self.button_br = statemachine.GFX['Quit_button']
        self.button_br_loc = (251, 248)
        self.cursor = statemachine.GFX['Cursor']
        self.cursor_loc = (22, 189)
        self.cursor_pos_tl = (22, 189)
        self.cursor_pos_tr = (251, 189)
        self.cursor_pos_bl = (22, 262)
        self.cursor_pos_br = (251, 262)
        self.next_state = "GAMEPLAY"

    def update(self, dt):

        if self.select:
            if self.position == settings.position['top_left']:
                self.next_state = "GAMEPLAY"
                self.done  = True

            if self.position == settings.position['bottom_right']:
                self.quit = True
            else:
                pass

        if self.direction == settings.direction['left']:
            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            else:
                pass

        if self.direction == settings.direction['right']:
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass

        if self.direction == settings.direction['up']:
            if self.position == settings.position['bottom_left']:
                self.cursor_loc = self.cursor_pos_tl
                self.position = settings.position['top_left']
            if self.position == settings.position['bottom_right']:
                self.cursor_loc = self.cursor_pos_tr
                self.position = settings.position['top_right']
            else:
                pass

        if self.direction == settings.direction['down']:
            if self.position == settings.position['top_left']:
                self.cursor_loc = self.cursor_pos_bl
                self.position = settings.position['bottom_left']
            if self.position == settings.position['top_right']:
                self.cursor_loc = self.cursor_pos_br
                self.position = settings.position['bottom_right']
            else:
                pass


        else:
            pass

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.direction = settings.direction['left']
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.direction = settings.direction['right']
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.direction = settings.direction['up']
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.direction = settings.direction['down']
            if keys[pg.K_SPACE]:
                self.select = True
            else:
                self.select = False


    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.back_ground,(0,0))
        surface.blit(self.button_tl,self.button_tl_loc)
        surface.blit(self.button_tr, self.button_tr_loc)
        surface.blit(self.button_bl, self.button_bl_loc)
        surface.blit(self.button_br, self.button_br_loc)
        surface.blit(self.cursor, self.cursor_loc)