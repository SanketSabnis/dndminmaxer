#!/usr/local/bin/python2.7
from evaluator import evaluate
import config
import copy
from combat import Combat


class Character(Combat):

    def __init__(self, **params):
        self.init_params = params
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

        if not hasattr(self, "attack_att"):
            self.attack_att = "str_mod"
        self.proficieny_bonus = self.get_proficiency_bonus()
        multiclass_levels = self.get_multiclass_levels()

        self.str_mod = (self.strength - 10) / 2
        self.dex_mod = (self.dexterity - 10) / 2
        self.con_mod = (self.consitution - 10) / 2
        self.int_mod = (self.initelligence - 10) / 2
        self.wis_mod = (self.wisdom - 10) / 2
        self.cha_mod = (self.charisma - 10) / 2
        self.initiative = self.dex_mod
        self.dmg_str = "%s(%s+%s)" % (self.attacks, self.weapon, self.str_mod)
        self.dmg_bonus = 0
        self.dmg_str = ""
        self.level = self.level - multiclass_levels

        if self.char_type == "barbarian":
            self.dmg_bonus += 2
            if self.level >= 9:
                self.dmg_bonus += 1
            if self.level >= 16:
                self.dmg_bonus += 1
            if self.level >= 20:
                self.strength += 4
                self.consitution += 4
                self.str_mod += 2
                self.con_mod += 2

        if self.char_type == "paladin":
            if self.level >= 11:
                self.smite += "+d8"

        self.attack_mod = getattr(self, self.attack_att)
        self.to_hit = self.attack_mod + self.proficieny_bonus
        self.add_adv()

        if hasattr(self, "hunter"):
            self.smite += "+d6"

        if hasattr(self, "hit_die"):
            hp = round(evaluate(self.hit_die))
            self.hit_points = evaluate("%s+%s+%s(%s+%s)" % (
                self.hit_die.replace("d", ""), hp, self.level - 1, hp, self.con_mod))
            if self.char_type == "barbarian" and self.fighting_style == "GWF":
                self.hit_points += self.fighter_level * (6 + self.con_mod)

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

        self.get_crit_chance()

    def check_feats(self, hit_chance, raw_hit_chance):
        if not hasattr(self, "feats") or not self.feats:
            return
        if "savage" in self.feats:
            num_die = self.weapon[0] if self.weapon[0] != "d" else 1
            if self.attacks > 1:
                self.dmg_str = "%s*(DropLowest%s%s+%s%s)+%s(%s*(%s+%s))" % (
                    hit_chance, num_die + 1, self.weapon,
                    self.attack_mod + self.dmg_bonus,
                    self.smite, self.attacks - 1, hit_chance,
                    self.weapon, self.attack_mod + self.dmg_bonus)
            else:
                self.dmg_str = "%s*(DropLowest%s%s+%s)" % (
                    hit_chance, num_die + 1, self.weapon, self.attack_mod + self.dmg_bonus)

        p_chance = self.check_gwm(raw_hit_chance, hit_chance, self.weapon, self.attacks, None)
        if "polearm_master" in self.feats or "xbow_expert" in self.feats:
            die = "d4" if "polearm_master" in self.feats else "d6"
            if "gwm" in self.feats or "gwm2" in self.feats:
                p_chance = self.check_gwm(raw_hit_chance, hit_chance, die, 1, self.dmg_str)
            else:
                self.dmg_str = "%s+(%s*(%s+%s%s))" % (self.dmg_str, hit_chance,
                                                      die, self.attack_mod + self.dmg_bonus,
                                                      self.reduced_smite())

        if hasattr(self, "path") and self.path == "zealot":
            self.dmg_str += "+%s*(d6+%s)" % (p_chance or hit_chance, self.level / 2)

    def check_gwm(self, raw_hit_chance, hit_chance, die, attacks, dmg_str):
        p_chance = None
        new_dmg_str = None
        if "gwm" in self.feats or "gwm2" in self.feats:
            penalty = 5 if "gwm" in self.feats else 2
            bonus_dmg = 10 if "gwm" in self.feats else (
                "%.4f" % evaluate("d%s" % die.split("d")[-1], self.fighting_style)
            )
            p_chance = min(1, (raw_hit_chance * 20 - penalty) / 20.0)
            p_attack = "(%s*(%s+%s+%s%s))" % (p_chance, die,
                                              self.attack_mod + self.dmg_bonus,
                                              bonus_dmg, self.smite)
            n_attack = "(%s*(%s+%s%s))" % (hit_chance, die,
                                           self.attack_mod + self.dmg_bonus, self.smite)
            np_attack = "%s+%s" % (p_attack, n_attack)
            p_dpr = self.evaluate_dmg_str("%s*(%s)" % (attacks, p_attack))
            np_dpr = self.evaluate_dmg_str(np_attack) if attacks > 1 else 0
            n_dpr = self.evaluate_dmg_str("%s*(%s)" % (attacks, n_attack))
            maxdpr = max(p_dpr, np_dpr, n_dpr)
            if maxdpr == p_dpr:
                new_dmg_str = "%s*%s" % (attacks, p_attack)
            elif maxdpr == np_dpr:
                new_dmg_str = np_attack
                p_chance = (hit_chance + p_chance) / 2.0
            else:
                new_dmg_str = "%s*%s" % (attacks, n_attack)
                p_chance = hit_chance

        if dmg_str:
            new_dmg_str = "%s+%s" % (dmg_str, new_dmg_str)
        if new_dmg_str:
            self.dmg_str = new_dmg_str
        return p_chance

    def check_def_feats(self, opp):
        if self.char_type == "barbarian":
            return round(opp.dpr(self) / 2.0)
        if not hasattr(self, "feats") or not self.feats:
            return 0
        if "ham" in self.feats and self.char_type != "barbarian":
            return opp.attacks * opp.hit_chance(self) * 3
        return 0

    def check_modifiers(self, hit_chance):
        if hasattr(self, "haste"):
            self.dmg_str += "+(%s*(%s+%s%s))" % (hit_chance, self.weapon,
                                                 self.attack_mod + self.dmg_bonus,
                                                 self.reduced_smite())

    def get_proficiency_bonus(self):
        if not hasattr(self, "level"):
            return 2
        char_level = self.character_level()
        mod = 1 if char_level % 4 == 0 else 2
        return char_level / 4 + mod

    def reduced_smite(self):
        plus_split = self.smite.split("+")
        smite_split = plus_split[1].split("d") if len(
            plus_split) > 1 and len(plus_split[1]) > 2 else [self.smite]
        reduced_smite = "+%sd%s" % (int(smite_split[0]) - 1,
                                    smite_split[1]) if len(smite_split) == 2 else self.smite
        return reduced_smite

    def get_crit_chance(self):
        die = 20.0
        crit_on = ["20"]
        if hasattr(self, "archetype") and self.archetype == "champion":
            level = self.level if self.char_type == "fighter" else getattr(self, "fighter_level", 0)
            if level >= 15:
                crit_on = ["20", "19", "18"]
            elif level >= 3:
                crit_on = ["20", "19"]
        crit_chance = len(crit_on) / die
        if hasattr(self, "adv"):
            crit_chance = 1 - ((die - len(crit_on)) / die)**2
        self.crit_chance = crit_chance
        return crit_chance

    def evaluate_dmg_str(self, dmg_str):
        crit_chance = self.get_crit_chance()
        crit_type = self.crit_type if hasattr(self, "crit_type") else "RAW"
        return evaluate(dmg_str, self.fighting_style, crit=True, crit_chance=crit_chance,
                        crit_type=crit_type)

    def add_adv(self):
        if self.char_type == "barbarian":
            self.adv = 1
        if hasattr(self, "adv"):
            self.to_hit += evaluate("DropLowest2d20-d20", crit=False)

    def increase_ability_scores(self, ability_increases_at, level_attr):
        if not ability_increases_at:
            return
        num_feats = len(self.feats) - 1 if hasattr(self, "feats") else 0
        ability_priority = ["strength", "consitution", "dexterity"]
        if self.attack_att == "dex_mod":
            ability_priority = list(reversed(ability_priority))
        ability_increases = 0
        for ability in ability_priority:
            for ability_increase_level in ability_increases_at[num_feats + ability_increases:]:
                if (getattr(self, ability) < 20
                        and getattr(self, level_attr) >= ability_increase_level):
                    setattr(self, ability, getattr(self, ability) + 2)
                    ability_increases += 1

    def character_level(self):
        return min(
            20,
            self.level + self.get_multiclass_levels()
        )

    def get_level_attacks(self, level_attr):
        level_attacks = [(1, 1), (5, 2)]
        ability_increases_at = [4, 8, 12, 16, 19]
        if level_attr == "fighter_level":
            level_attacks.extend([(11, 3), (20, 4)])
            ability_increases_at.extend([6, 14])
            ability_increases_at = sorted(ability_increases_at)
        for level, attacks in level_attacks:
            if getattr(self, level_attr) >= level:
                if hasattr(self, "attacks"):
                    self.attacks = max(self.attacks, attacks)
                else:
                    self.attacks = attacks
        return ability_increases_at

    def get_multiclass_levels(self):
        multiclass_levels = 0
        if hasattr(self, "level") and not hasattr(self, "attacks"):
            variables = copy.deepcopy(vars(self))
            for att in variables:
                if att.endswith("level"):
                    ability_increases_at = self.get_level_attacks(att)
                    self.increase_ability_scores(ability_increases_at, att)
                    if att.endswith("_level"):
                        multiclass_levels += getattr(self, att)
        return multiclass_levels
