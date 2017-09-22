from random import randint
from settings import *


player_img1 = statemachine.GFX['female_right']
player_img2 = statemachine.GFX['female_right_l']
player_img3 = statemachine.GFX['female_right_r']

player_stats = {'str' : 10, 'str mod' : 0, 'dex' : 10, 'dex mod' : 0, 'con' : 10, 'con mod' : 0,
                'int' : 10, 'int mod' : 0, 'wis' : 10, 'wis mod' : 0, 'cha' : 10, 'cha mod' : 0,
                'total_hit_points' : 10, 'current_hit_points' : 10, 'exp' : 0, 'level' : 1,
                'speed' : 30, 'AC' : 10, 'melee_dam_low' : 1, 'melee_dam_high' : 4,
                'hit_die_low' : 1, 'hit_die_high' : 8, 'prof_points' : 0, 'atr_points' : 0,
                'party' : {'party1' : 'player', 'party2' : None, 'party3' : None},
                'party2_stats' : {}, 'party3_stats' : {}, 'img1' : player_img1, 'img2' : player_img2, 'img3' : player_img3}




class Player_bat(pg.sprite.Sprite):
    def __init__(self, game, dict, loc):
        self.groups = game.party
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.stats = dict
        self.img = self.stats['img1']
        self.img1 = self.stats['img1']
        self.img2 = self.stats['img2']
        self.img3 = self.stats['img3']
        self.loc = loc
        self.health = self.stats['current_hit_points']
        self.init = 0
        self.turn = False
        self.done = False
        self.player = True




    def attack(self, target):
        atk_roll = randint(1, 20) + self.stats['str mod']
        if atk_roll >= target.stats['AC']:
            dam_roll = randint(self.stats['melee_dam_low'], self.stats['melee_dam_high']) + self.stats['str mod']
            target.health -= dam_roll
            self.game.damage_done = True
            self.game.damage_amount = dam_roll
            self.game.damage_loc = target.loc
        else:
            self.game.miss = True
            self.game.miss_loc = target.loc
        self.done = True
        self.turn = False

    def init_roll(self):
        roll = randint(1, 10)
        self.init = roll  + self.stats['dex mod']
