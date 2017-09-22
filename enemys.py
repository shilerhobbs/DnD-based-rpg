import sys
import pygame as pg
import statemachine
import settings
from os import path
from settings import *
from random import randint
import sprites
import tilemap
from player_stats import *






enemy1 = None
enemy2 = None
enemy3 = None
enemy4 = None
enemy5 = None
enemy_list = [enemy1, enemy2, enemy3, enemy4, enemy5]



#####  bat stats
bat_img1 = statemachine.GFX['bat_left']
bat_img2 = statemachine.GFX['bat_left_l']
bat_img3 = statemachine.GFX['bat_left_r']

bat_stats = {'str' : 2, 'str mod' : -4, 'dex' : 15, 'dex mod' : 2, 'con' : 8, 'con mod' : -1,
                'int' : 2, 'int mod' : -4, 'wis' : 12, 'wis mod' : 1, 'cha' : 4, 'cha mod' : -3,
                'total_hit_points' : 3, 'current_hit_points' : 3, 'exp' : 10,
                'speed' : 5, 'AC' : 12, 'atk_dam_low' : 1, 'atk_dam_high' : 2, 'atk_bonus' : 0,
             'img1' : bat_img1, 'img2' : bat_img2, 'img3' : bat_img3}


#####  bat stats
larva_img1 = statemachine.GFX['larva_left']
larva_img2 = statemachine.GFX['larva_left_l']
larva_img3 = statemachine.GFX['larva_left_r']

larva_stats = {'str' : 2, 'str mod' : -4, 'dex' : 15, 'dex mod' : 2, 'con' : 8, 'con mod' : -1,
                'int' : 2, 'int mod' : -4, 'wis' : 12, 'wis mod' : 1, 'cha' : 4, 'cha mod' : -3,
                'total_hit_points' : 3, 'current_hit_points' : 3, 'exp' : 10,
                'speed' : 5, 'AC' : 12, 'atk_dam_low' : 1, 'atk_dam_high' : 2, 'atk_bonus' : 0,
             'img1' : larva_img1, 'img2' : larva_img2, 'img3' : larva_img3}



bandit_1_img1 = statemachine.GFX['bandit_1_left']
bandit_1_img2 = statemachine.GFX['bandit_1_left_l']
bandit_1_img3 = statemachine.GFX['bandit_1_left_r']

bandit_1_stats = {'str' : 11, 'str mod' : 0, 'dex' : 12, 'dex mod' : 1, 'con' : 12, 'con mod' : 1,
                'int' : 10, 'int mod' : 0, 'wis' : 10, 'wis mod' : 0, 'cha' : 10, 'cha mod' : 0,
                'total_hit_points' : 11, 'current_hit_points' : 11, 'exp' : 25,
                'speed' : 30, 'AC' : 12, 'atk_dam_low' : 2, 'atk_dam_high' : 7, 'atk_bonus' : 0,
             'img1' : bandit_1_img1, 'img2' : bandit_1_img2, 'img3' : bandit_1_img3}

# Scimitar: Melee Weapon Attack: +3 to hit, reach 5 ft., one target. Hit: 4 (1d6 + 1) slashing damage.
# Light Crossbow: Ranged Weapon Attack: +3 to hit, range 80 ft./320 ft., one target. Hit: 5 (1d8 + 1) piercing damage.


bandit_2_img1 = statemachine.GFX['bandit_1_left']
bandit_2_img2 = statemachine.GFX['bandit_1_left_l']
bandit_2_img3 = statemachine.GFX['bandit_1_left_r']

bandit_2_stats = {'str' : 11, 'str mod' : 0, 'dex' : 12, 'dex mod' : 1, 'con' : 12, 'con mod' : 1,
                'int' : 10, 'int mod' : 0, 'wis' : 10, 'wis mod' : 0, 'cha' : 10, 'cha mod' : 0,
                'total_hit_points' : 11, 'current_hit_points' : 11, 'exp' : 25,
                'speed' : 30, 'AC' : 12, 'atk_dam_low' : 2, 'atk_dam_high' : 7, 'atk_bonus' : 0,
             'img1' : bandit_2_img1, 'img2' : bandit_2_img2, 'img3' : bandit_2_img3}

bandit_boss_img1 = statemachine.GFX['bandit_1_left']
bandit_boss_img2 = statemachine.GFX['bandit_1_left_l']
bandit_boss_img3 = statemachine.GFX['bandit_1_left_r']

bandit_boss_stats = {'str' : 15, 'str mod' : 2, 'dex' : 16, 'dex mod' : 3, 'con' : 14, 'con mod' : 2,
                'int' : 14, 'int mod' : 2, 'wis' : 11, 'wis mod' : 0, 'cha' : 14, 'cha mod' : 2,
                'total_hit_points' : 65, 'current_hit_points' : 65, 'exp' : 450,
                'speed' : 30, 'AC' : 15, 'atk_dam_low' : 4, 'atk_dam_high' : 9, 'atk_bonus' : 0,
             'img1' : bandit_boss_img1, 'img2' : bandit_boss_img2, 'img3' : bandit_boss_img3}

# Multiattack: The captain makes three melee attacks: two with its scimitar and one with its dagger. Or the captain makes two ranged attacks with its daggers.
# Scimitar: Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 6 (1d6 + 3) slashing damage.
# Dagger: Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 5 (1d4 + 3) piercing damage.






enemy_dict = {'bat' : bat_stats, 'larva' : larva_stats, 'bandit1' : bandit_1_stats,
              'bandit2' : bandit_2_stats, 'banditboss' : bandit_boss_stats}


encounter_dict = {1 : {1 : ['bat', 'bat', 'bat', '', ''],
                       2 : ['bat', 'bat', '', '', ''],
                       3 : ['bat', '', '', '', ''],
                       4 : ['larva', 'larva', 'larva', '', ''],
                       5 : ['larva', 'larva', '', '', ''],
                       6 : ['larva', '', '', '', ''],
                       7 : ['bandit1', '', '', '', ''],
                       8 : ['bandit2', '', '', '', ''],
                       9 : ['bandit1', 'bandit2', '', '', ''],
                       10 : ['banditboss', '', '', '', '']




                       },

                  2 : {}




                  }




class Enemy(pg.sprite.Sprite):
    def __init__(self, game, dict, loc):
        self.groups = game.enemy
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
        self.target = None
        self.player = False



    def take_turn(self):

        self.attack()
        self.turn = False
        self.done = True

    def attack(self):

        self.get_target()
        atk_roll = randint(1, 20) + self.stats['atk_bonus']
        if atk_roll >= self.target.stats['AC']:
            dam_roll = randint(self.stats['atk_dam_low'], self.stats['atk_dam_high'])
            self.target.stats['current_hit_points'] -= dam_roll
            self.game.damage_done = True
            self.game.damage_amount = dam_roll
            self.game.damage_loc = self.target.loc
        else:
            self.game.miss = True
            self.game.miss_loc = self.target.loc

    def init_roll(self):
        roll = randint(1, 10)
        self.init = roll + self.stats['dex mod']

    def get_target(self):
        targets = []
        for party in self.game.party:
            targets.append(party.stats['current_hit_points'])
        least_health = min(sorted(targets))
        for party in self.game.party:
            if party.stats['current_hit_points'] == least_health:
                self.target = party
            else:
                pass
