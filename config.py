from player import Character

smite = "3d8"
bless = "d4"

monster = {
    "strength": 18,
    "dexterity": 11,
    "consitution": 16,
    "initelligence": 6,
    "wisdom": 11,
    "charisma": 8,
    "level": 3,
    "ac": 14,
    "weapon": "2d12",
    "hit_points": 176,
    "attacks": 1,
    "profiency_bonus": 0,
    "fighting_style": None,
    "smite": "",
    "name": "Minotaur",
    "bless": "",
    "bane": ""
}

paladin = {
    "strength": 16,
    "dexterity": 14,
    "consitution": 16,
    "initelligence": 8,
    "wisdom": 12,
    "charisma": 8,
    "level": 6,
    "primary_attr": "str_mod",
    "ac": 17,
    "weapon": "d8",
    "hit_die": "d10",
    "fighting_style": None,
    "smite": "",
    "bless": "",
    "bane": ""
}


fighter = {
    "strength": 16,
    "dexterity": 14,
    "consitution": 16,
    "initelligence": 8,
    "wisdom": 12,
    "charisma": 8,
    "level": 4,
    "primary_attr": "str_mod",
    "ac": 17,
    "weapon": "d8",
    "hit_die": "d10",
    "fighting_style": None,
    "smite": "",
    "bless": "",
    "bane": ""
}

barbarian = {
    "strength": 16,
    "dexterity": 14,
    "consitution": 16,
    "initelligence": 8,
    "wisdom": 12,
    "charisma": 8,
    "level": 8,
    "primary_attr": "str_mod",
    "ac": 17,
    "weapon": "d12",
    "hit_die": "d12",
    "fighting_style": None,
    "smite": "",
    "bless": "",
    "bane": ""
}
players = [
    Character(name="Great Axe GWM2", path="zealot", feats=["gwm2"],
              char_type="barbarian", weapon="d12", crit_type="HBC"),
    Character(name="Polearm Master GWF", path="zealot", feats=["polearm_master"],
              char_type="barbarian", weapon="d10", crit_type="HBC", fighting_style="GWF",
              fighter_level=3, level=5, archetype="champion"),
    Character(name="Great Axe GWM2 GWF", feats=["gwm2"], char_type="barbarian",
              weapon="d12", path="zealot", crit_type="HBC", fighting_style="GWF",
              fighter_level=3, level=5, archetype="champion"),
    Character(name="Polearm Master GWM2", path="zealot", feats=["polearm_master", "gwm2"],
              char_type="barbarian", weapon="d10", crit_type="HBC", strength=16),
    Character(name="Polearm Master GWF GWM2", path="zealot", feats=["polearm_master", "gwm2"],
              char_type="barbarian", weapon="d10", crit_type="HBC", fighting_style="GWF",
              fighter_level=3, level=5, archetype="champion", strength=16)
]
'''
old_players = [
    Character(name="Great Axe GWM2 Adv", feats=["gwm2"], char_type="fighter", fighting_style="GWF",
                   weapon="d12", archetype="battlemaster", adv=1),
    Character(name="Great Axe GWM2", feats=["gwm2"], char_type="fighter", fighting_style="GWF",
                   weapon="d12", archetype="battlemaster"),
    Character(name="SnB HAM", feats=["ham"], fighting_style="DUELLING", char_type="fighter",
                   weapon="d8"),
    Character(name="Archery SS", feats=["xbow_expert", "gwm"],
                   fighting_style="ARCHERY", char_type="fighter", attack_att="dex_mod",
                   dexterity=16, ac=16, weapon="d6"),
    Character(name="Great Sword GWM2", feats=["gwm2"], char_type="fighter",
                   fighting_style="GWF", weapon="2d6"),
    Character(name="Great Axe GWM2", feats=["gwm2"], char_type="fighter", fighting_style="GWF",
                   weapon="d12"),
    Character(name="Archery Xbow SS2", feats=["xbow_expert", "gwm2"],
                   fighting_style="ARCHERY", char_type="fighter", attack_att="dex_mod",
                   dexterity=16, ac=16, weapon="d6"),
    Character(name="Great Sword GWM2", feats=["gwm2"], char_type="fighter",
              fighting_style="DEFENSE", weapon="2d6")
]
'''
opponent = Character(char_type="monster")
