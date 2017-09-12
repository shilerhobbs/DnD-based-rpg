import sys
import pygame as pg
import statemachine
import settings
from os import path
from settings import *
import sprites
import tilemap


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
                self.next_state = "STAT_F"
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



class Gameplay(statemachine.GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.event = pg.sprite.Group()
        self.encounter = pg.sprite.Group()
        self.dialog = pg.sprite.Group()
        # self.player = sprites.Player(self, 0, 0)

    def make_map(self):
        for sprite in self.all_sprites:
            self.all_sprites.remove(sprite)
        for wall in self.walls:
            self.walls.remove(wall)
        for event in self.event:
            self.event.remove(event)
        for dialog in self.dialog:
            self.dialog.remove(dialog)
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
                                  tile_object.properties['location'])

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




    def startup(self, persistent):
        self.persist = persistent
        self.make_map()
        self.info1 = 'wasd to move'
        self.info2 = 'space to interact'
        self.dialog_box(self.info1,self.info2,None,None,None,None,None,None)
        if not self.player.info:
            self.player.dialog_text1 = self.info1
            self.player.dialog_text2 = self.info2
            self.player.dialog = True





    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if self.player.dialog:
            self.dialog_box(self.player.dialog_text1, self.player.dialog_text2, self.player.dialog_text3,
                            self.player.dialog_text4, self.player.dialog_text5, self.player.dialog_text6,
                            self.player.dialog_text7, self.player.dialog_text8)
        if not self.player.dialog:
            self.player.get_keys()
        if self.player.map_change:

            settings.play_map = map_dict[self.player.map_change_dest]
            self.make_map()
        if self.player.battle:
            self.next_state = "BATTLE"
            self.done = True




    def update(self, dt):
        self.player.update(dt)
        self.camera.update(self.player)

    def draw(self, surface):
        surface.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            surface.blit(sprite.image, self.camera.apply(sprite))

        ######  debug
        CYAN = (0, 255, 255)
        ORANGE = (255, 165, 0)
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
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
        self.cursor_loc = (-2,269)
        self.cursor_pos_tl = (-2, 269)
        self.cursor_pos_tr = (121, 269)
        self.cursor_pos_bl = (-2, 295)
        self.cursor_pos_br = (121, 295)
        self.layer_1 = statemachine.GFX['Mountains_battleback']
        self.layer_2 = statemachine.GFX['Battle_menu_back']
        self.layer_2_loc = (0, 264)

        self.next_state = "GAMEPLAY"

    def update(self, dt):

        if self.select:
            ###   ATTACK
            if self.position == settings.position['top_left']:
                pass
            ###   ITEM
            if self.position == settings.position['top_right']:
                pass
            ###   EQUIP
            if self.position == settings.position['bottom_left']:
                pass
            ###   FLEE
            if self.position == settings.position['bottom_right']:
                self.done = True
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
        surface.blit(self.layer_1,(0,0))
        surface.blit(self.layer_2,self.layer_2_loc)
        surface.blit(self.button_tl,self.button_tl_loc)
        surface.blit(self.button_tr, self.button_tr_loc)
        surface.blit(self.button_bl, self.button_bl_loc)
        surface.blit(self.button_br, self.button_br_loc)
        surface.blit(self.cursor, self.cursor_loc)



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