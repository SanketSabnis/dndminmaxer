from evaluator import evaluate

class Combat():

    def dpr(self, opp=None):
        hit_chance = self.hit_chance(opp)
        self.dmg_str = "%s(%s*(%s+%s%s))"% (self.attacks, hit_chance, self.weapon, self.str_mod + self.dmg_bonus, self.smite)
        self.check_modifiers(hit_chance)
        self.check_feats(hit_chance, self.raw_hit_chance(opp))
        return evaluate(self.dmg_str, fighting_style=self.fighting_style)

    def dtpr(self, opp):
        dmg_reduction = self.check_def_feats(opp)
        #if dmg_reduction: print dmg_reduction
        return opp.dpr(self) - dmg_reduction

    def ris(self, opp):
        return self.hit_points/float(self.dtpr(opp))

    def eff(self, opp):
        return (self.dpr(opp)- self.dtpr(opp)) * self.ris(opp)/opp.ris(self)

    def dmg(self, opp):
        return (self.dpr(opp) * self.ris(opp))

    def raw_hit_chance(self, opp):
        return  (20 - (opp.ac - (self.to_hit + evaluate(self.bless or "0"))))/ 20.0

    def hit_chance(self, opp):
        return min(1, self.raw_hit_chance(opp))
