#!/usr/bin/python2.7
import os
import sys
from config import *
from player import *


if __name__ == "__main__":
    p1 = Character(name="Polearm + GWF",feats=["polearm_master"],fighting_style="GWF",default=1)
    p2 = Character(name="Sword and Board",fighting_style="DUELLING",weapon="d8",consitution=16,default=1)
    p3 = Character(name="Polearm + Defense",feats=["polearm_master"],fighting_style="DEFENSE",default=1)
    p4 = Character(name="GreatSword + GWF",fighting_style="GWF",weapon="2d6",default=1)
    p5 = Character(name="GreatSword + Defense",fighting_style="DEFENSE",weapon="2d6",default=1)
    p6 = Character(name="Polearm + Duelling (Cheese)",feats=["polearm_master"],fighting_style="DUELLING",weapon="d6",default=1)
    p7 = Character(name="Great Axe",fighting_style="GWF",weapon="d12",default=1)
    p8 = Character(name="TANK",fighting_style="DUELLING",weapon="d8",default=1,ac=18,feats=["ham"])
    p9 = Character(name="Cleric",consitution=19,weapon="d12",attacks=1,strength=17,default=1)
    m = Character(monster=1)
    players = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
    stats = ["name", "dpr ", "dtpr", "ris ", "eff ", "dmg ", "odmg"]
    len_max_name = max(len(p.name) for p in players)
    headers = []
    for x in stats:
        headers.append("%s%s" % (x.upper(),(" "*(len_max_name - len("name") +5) if x =="name" else "\t ")))
    header_str= "".join(headers)
    print "%s\n%s"% (header_str, "-"*(int(1.25*len(header_str))))
    for p in players:
        num_spaces = (len_max_name - len(p.name))+5
        tokens = []
        for stat in stats:
            if stat == "name":
                val = p.name
                tokens.append("%s%s"%(val," "*num_spaces))
            else:
                val = getattr(p, stat.strip())(m)
                tokens.append("%.3f\t "% (val))
        print "".join(tokens)

