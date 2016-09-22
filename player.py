#!/usr/local/bin/python2.7
import os
import sys
from config import *


class Combat():

    def dpr(self, opp=None):
        hit_chance = self.hit_chance(opp)
        self.dmg_str = "%s(%s*(%s+%s%s))"% (self.attacks, hit_chance, self.weapon, self.str_mod + self.dmg_bonus, self.smite)
        self.check_feats(hit_chance)
        return evaluate(self.dmg_str, fighting_style=self.fighting_style)

    def dtpr(self, opp):
        dmg_reduction = self.check_def_feats(opp)
        #if dmg_reduction: print dmg_reduction
        return opp.dpr(self) - dmg_reduction

    def ris(self, opp):
        return self.hit_points/float(self.dtpr(opp))

    def eff(self, opp):
        return (self.dpr(opp) * self.ris(opp))/float(opp.ris(self))

    def dmg(self, opp):
        return (self.dpr(opp) * self.ris(opp))

    def hit_chance(self, opp=None):
        return min(1, (20 - (opp.ac - self.to_hit))/ float(20)) if opp else 1

class Character(Combat):

    def __init__(self, **params):
        if "default" in params:
            for k,v in player.iteritems():
                params.setdefault(k, v)
        if "monster" in params:
            for k,v in monster.iteritems():
                params.setdefault(k, v)
        for att in params:
            if att in ["default", "monster"]: continue
            setattr(self,att,params[att])
        if hasattr(self, "feats"):
            self.strength -= (len(self.feats)-1)*2

        self.proficieny_bonus=  2 if self.level < 5 else 3 if self.level < 9 else 4 if self.level < 13 else 5 if self.level < 17 else 5
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
        self.dmg_str = "" 
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
                self.dmg_str = "%s*(DropLowest%s%s+%s%s)+%s(%s*(%s+%s%s))"% (hit_chance,num_die+1, self.weapon, self.str_mod+ self.dmg_bonus, self.smite, self.attacks-1, hit_chance, self.weapon, self.str_mod+ self.dmg_bonus, self.smite)
            else:
                self.dmg_str = "%s*(DropLowest%s%s+%s%s)"% (hit_chance, num_die+1,self.weapon, self.str_mod+ self.dmg_bonus, self.smite)
        if "gwm" in self.feats:
            p_attack = "(%s*(%s+%s+10%s))"% ((hit_chance*20-5)/20.0, self.weapon, self.str_mod + self.dmg_bonus, self.smite)
            n_attack = "(%s*(%s+%s%s))"% (hit_chance, self.weapon, self.str_mod + self.dmg_bonus, self.smite)
            np_attack = "%s+%s"% (p_attack, n_attack)
            p_dpr = evaluate("2*(%s)"%p_attack, self.fighting_style)
            np_dpr = evaluate(np_attack, self.fighting_style)
            n_dpr = evaluate("2*(%s)"% n_attack, self.fighting_style)
            maxdpr = max(p_dpr, np_dpr, n_dpr)
            if maxdpr == p_dpr:
                self.dmg_str = "2*%s"%p_attack
            elif maxdpr == np_dpr:
                self.dmg_str = np_attack
            else:
                self.dmg_str = "2*%s"% n_attack
            #self.dmg_str = "%s+(%s*%s(%s+%s))"% (self.dmg_str, self.crit_chance, hit_chance, self.weapon, self.str_mod+ self.dmg_bonus)
        if "polearm_master" in self.feats:
            if "gwm" in self.feats:
                p_attack ="%s*(d4+%s+10%s)"% ((hit_chance*20-5)/20.0, self.str_mod + self.dmg_bonus, self.smite)
                n_attack = "%s*(d4+%s%s)"% (hit_chance, self.str_mod+ self.dmg_bonus, self.smite)
                p_dpr = evaluate(p_attack, self.fighting_style)
                n_dpr = evaluate(n_attack, self.fighting_style)
                maxdpr = max(p_dpr, n_dpr)
                if maxdpr == p_dpr:
                    self.dmg_str = "%s+%s"%(self.dmg_str, p_attack)
                else:
                    self.dmg_str = "%s+%s"%(self.dmg_str, n_attack)
            else:
                self.dmg_str = "%s+(%s*(d4+%s%s))"% (self.dmg_str, hit_chance, self.str_mod+ self.dmg_bonus, self.smite)


    def check_def_feats(self, opp):
        if not hasattr(self,"feats") or not self.feats: return 0
        if "ham" in self.feats:
            return opp.attacks*opp.hit_chance(self)*3
        return 0
