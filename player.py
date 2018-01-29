#!/usr/local/bin/python2.7
import os
import sys
from evaluator import evaluate
import config
from combat import Combat


class Character(Combat):

    def __init__(self, **params):
        if params.get("char_type"):
            for k, v in getattr(config, params["char_type"]).iteritems():
                setattr(self, k, v)

        for att in params.get("modifiers", []):
            value = getattr(config, att) if hasattr(config, att) else 1
            if att == "smite":
                value = "+%s" % value
            setattr(self, att, value)

        for att, value in params.iteritems():
            if hasattr(self, att) and not value:
                delattr(self, att)
            setattr(self, att, value)

        # if hasattr(self, "feats"):
        #    self.strength -= (len(self.feats)-1)*2

        self.proficieny_bonus = self.get_proficiency_bonus()
        if not hasattr(self, "attack_att"):
            self.attack_att = "str_mod"
        self.str_mod = (self.strength - 10) / 2
        self.dex_mod = (self.dexterity - 10) / 2
        self.con_mod = (self.consitution - 10) / 2
        self.int_mod = (self.initelligence - 10) / 2
        self.wis_mod = (self.wisdom - 10) / 2
        self.cha_mod = (self.charisma - 10) / 2
        self.initiative = self.dex_mod
        self.attack_mod = getattr(self, self.attack_att)
        self.to_hit = self.attack_mod + self.proficieny_bonus
        self.dmg_str = "%s(%s+%s)" % (self.attacks, self.weapon, self.str_mod)
        self.dmg_bonus = 0
        self.dmg_str = ""
        if hasattr(self, "adv"):
            self.to_hit += evaluate("DropLowest2d20-d20", crit=False)
        if hasattr(self, "hunter"):
            self.smite += "+d6"

        if hasattr(self, "hit_die"):
            hp = round(evaluate(self.hit_die))
            no_of_players = self.count if hasattr(self, "count") else 1
            self.hit_points = no_of_players * evaluate("%s+%s+%s(%s+%s)" % (
                self.hit_die.replace("d", ""), hp, self.con_mod, self.level - 1, self.con_mod))

        if hasattr(self, "fighting_style"):
            if self.fighting_style == "DEFENSE":
                self.ac += 1
            if self.fighting_style == "DUELLING":
                self.ac += 2
                self.dmg_bonus += 2
            if self.fighting_style == "ARCHERY":
                self.to_hit += 2

        if hasattr(self, "shield"):
            self.ac += self.shield

    def check_feats(self, hit_chance=1, raw_hit_chance=1.25):
        if not hasattr(self, "feats") or not self.feats:
            return
        if "polearm_master" in self.feats:
            self.attacks = int(self.attacks)
        if "savage" in self.feats:
            num_die = self.weapon[0] if self.weapon[0] != "d" else 1
            if self.attacks > 1:
                self.dmg_str = "%s*(DropLowest%s%s+%s)+%s(%s*(%s+%s))" % (
                    hit_chance, num_die + 1, self.weapon, self.attack_mod + self.dmg_bonus,
                    self.smite, self.attacks - 1, hit_chance,
                    self.weapon, self.str_mod + self.dmg_bonus)
            else:
                self.dmg_str = "%s*(DropLowest%s%s+%s)" % (
                    hit_chance, num_die + 1, self.weapon, self.attack_mod + self.dmg_bonus)

        if "gwm" in self.feats or "gwm2" in self.feats:
            penalty = 5 if "gwm" in self.feats else self.proficieny_bonus
            bonus_dmg = 10 if "gwm" in self.feats else "%s*d%s" % (
                self.proficieny_bonus / 2, self.weapon.split("d")[-1]
            )
            p_chance = min(1, (raw_hit_chance * 20 - penalty) / 20.0)
            p_attack = "(%s*(%s+%s+%s%s))" % (p_chance, self.weapon,
                                              self.attack_mod + self.dmg_bonus,
                                              bonus_dmg, self.smite)
            n_attack = "(%s*(%s+%s%s))" % (hit_chance, self.weapon,
                                           self.attack_mod + self.dmg_bonus, self.smite)
            np_attack = "%s+%s" % (p_attack, n_attack)
            p_dpr = evaluate("%s*(%s)" % (self.attacks, p_attack), self.fighting_style)
            np_dpr = evaluate(np_attack, self.fighting_style) if self.attacks > 1 else 0
            n_dpr = evaluate("%s*(%s)" % (self.attacks, n_attack), self.fighting_style)
            maxdpr = max(p_dpr, np_dpr, n_dpr)
            if maxdpr == p_dpr:
                self.dmg_str = "%s*%s" % (self.attacks, p_attack)
            elif maxdpr == np_dpr:
                self.dmg_str = np_attack
            else:
                self.dmg_str = "%s*%s" % (self.attacks, n_attack)

        if "polearm_master" in self.feats or "xbow_expert" in self.feats:
            die = "d4" if "polearm_master" in self.feats else "d6"
            die += "+d8" if "hunter" in self.feats else ""
            if "gwm" in self.feats:
                p_attack = "%s*(%s+%s+%s%s)" % (p_chance, die,
                                                self.attack_mod + self.dmg_bonus,
                                                bonus_dmg, self.smite)
                n_attack = "%s*(%s+%s%s)" % (hit_chance, die,
                                             self.attack_mod + self.dmg_bonus, self.smite)
                p_dpr = evaluate(p_attack, self.fighting_style)
                n_dpr = evaluate(n_attack, self.fighting_style)
                maxdpr = max(p_dpr, n_dpr)
                if maxdpr == p_dpr:
                    self.dmg_str = "%s+%s" % (self.dmg_str, p_attack)
                else:
                    self.dmg_str = "%s+%s" % (self.dmg_str, n_attack)
            else:
                self.dmg_str = "%s+(%s*(%s+%s%s))" % (self.dmg_str, hit_chance,
                                                      die, self.attack_mod + self.dmg_bonus,
                                                      self.reduced_smite())

    def check_def_feats(self, opp):
        if not hasattr(self, "feats") or not self.feats:
            return 0
        if "ham" in self.feats:
            return opp.attacks * opp.hit_chance(self) * 3
        return 0

    def check_modifiers(self, hit_chance):
        if hasattr(self, "haste"):
            self.dmg_str += "+(%s*(%s+%s%s))" % (hit_chance, self.weapon,
                                                 self.attack_mod + self.dmg_bonus, self.reduced_smite())

    def get_proficiency_bonus(self):
        if not hasattr(self, "level"):
            return 2
        mod = 1 if self.level % 4 == 0 else 2
        return self.level / 4 + mod
        #2 if self.level < 5 else 3 if self.level < 9 else 4 if self.level < 13 else 5 if self.level < 17 else 6

    def reduced_smite(self):
        plus_split = self.smite.split("+")
        smite_split = plus_split[1].split("d") if len(
            plus_split) > 1 and len(plus_split[1]) > 2 else [self.smite]
        reduced_smite = "+%sd%s" % (int(smite_split[0]) - 1,
                                    smite_split[1]) if len(smite_split) == 2 else self.smite
        return reduced_smite
