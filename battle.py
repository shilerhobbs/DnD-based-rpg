import sys
import pygame as pg
import statemachine
import settings
from os import path
from settings import *



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
            if self.position == settings.position['top_left']:
                pass

            if self.position == settings.position['bottom_right']:
                pass
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