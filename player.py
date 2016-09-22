#!/usr/local/bin/python2.7
import os
import sys
from config import *


class Combat():

    def dpr(self, opp=None):
        hit_chance = self.hit_chance(opp)
        self.dmg_str = "%s(%s*(%s+%s))"% (self.attacks, hit_chance, self.weapon, self.str_mod + self.dmg_bonus)
        self.check_feats(hit_chance)
        return evaluate(self.dmg_str, fighting_style=self.fighting_style)

    def dtpr(self, opp):
        dmg_reduction = self.check_def_feats(opp)
        #if dmg_reduction: print dmg_reduction
        return opp.dpr(self) - dmg_reduction

    def ris(self, opp):
        return self.hit_points/float(self.dtpr(opp))

    def eff(self, opp):
        return (self.dpr(opp) * self.ris(opp))/opp.ris(self)

    def dmg(self, opp):
        return (self.dpr(opp) * self.ris(opp))

    def hit_chance(self, opp=None):
        return min(1, (20 - (opp.ac - self.to_hit))/ float(20)) if opp else 1

class Character(Combat):

    def __init__(self, **params):
        if "default" in params:
            self.strength = 18
            self.dexterity = 8
            self.consitution = 14
            self.initelligence = 8
            self.wisdom = 10
            self.charisma = 16
            self.level = 5
            self.primary_attr = "str_mod"
            self.ac = 17
            self.weapon = "d10"
            self.hit_die = "d10"
            self.attacks = 2
            self.proficieny_bonus = 2 if self.level < 5 else 3 if self.level < 9 else 4 if self.level < 13 else 5 if self.level < 17 else 5
        if "monster" in params:
            self.strength = 18
            self.dexterity = 11
            self.consitution = 16
            self.initelligence = 6
            self.wisdom = 11
            self.charisma = 9
            self.level = 9
            self.ac = 14
            self.weapon = "2d12"
            self.hit_points = 76
            self.attacks = 1
            self.proficieny_bonus = 2
            self.fighting_style = None
        if "attributes" in params:
            attributes = params["attributes"]
            self.strength = attributes[0]
            self.dexterity = attributes[1]
            self.consitution = attributes[2]
            self.initelligence = attributes[3]
            self.wisdom = attributes[4]
            self.charisma = attributes[5]
        for att in params:
            if att == "default": continue
            setattr(self,att,params[att])
        self.primary_attr = "str_mod"
        self.str_mod = (self.strength - 10)/2
        self.dex_mod = (self.dexterity - 10)/2
        self.con_mod = (self.consitution -10)/2
        self.int_mod = (self.initelligence - 10)/2
        self.wis_mod = (self.wisdom - 10)/2
        self.cha_mod = (self.charisma -10)/2
        self.initiative = self.dex_mod
        self.to_hit = getattr(self, self.primary_attr) + self.proficieny_bonus
        self.dmg_str = "%s(%s+%s)"% (self.attacks, self.weapon, self.str_mod)
        self.dmg_bonus  = 0
        self.dmg_str = "%s(%s+%s+%s)"% (self.attacks, self.weapon, self.str_mod, self.dmg_bonus)
        self.crit_chance = 0.05
        if hasattr(self, "hit_die"):
            self.hit_points = evaluate("%s+%s+%s(%s+%s)"%(self.hit_die.replace("d",""), self.con_mod, self.level-1, self.hit_die, self.con_mod))
        if hasattr(self, "fighting_style"):
            if self.fighting_style == "DEFENSE":
                self.ac += 1
            if self.fighting_style == "DUELLING":
                self.ac += 2
                self.dmg_bonus +=2
        if hasattr(self, "shield"):
            self.ac += self.shield


    def check_feats(self, hit_chance=1):
        if not hasattr(self,"feats") or not self.feats: return
        if "savage" in self.feats:
            num_die = self.weapon[0] if self.weapon[0] !="d" else 1 
            if self.attacks >1:
                self.dmg_str = "%s*(DropLowest%s%s+%s)+%s(%s*(%s+%s))"% (hit_chance,num_die+1, self.weapon, self.str_mod+ self.dmg_bonus, self.attacks-1, hit_chance, self.weapon, self.str_mod+ self.dmg_bonus)
            else:
                self.dmg_str = "%s*(DropLowest%s%s+%s)"% (hit_chance, num_die+1,self.weapon, self.str_mod+ self.dmg_bonus)
        if "polearm_master" in self.feats:
            self.dmg_str = "%s+(%s*(d4+%s))"% (self.dmg_str, hit_chance, self.str_mod+ self.dmg_bonus)
        if "gwm" in self.feats:
            self.dmg_str = "%s+(%s*%s(%s+%s))"% (self.dmg_str, self.crit_chance, hit_chance, self.weapon, self.str_mod+ self.dmg_bonus)

    def check_def_feats(self, opp):
        if not hasattr(self,"feats") or not self.feats: return 0
        if "ham" in self.feats:
            return opp.attacks*opp.hit_chance(self)*3
        return 0
