#!/usr/bin/python2.7
import os
import sys
from config import *
from player import *


if __name__ == "__main__":
    p1 = Character(name="Polearm + GWF",feats=["polearm_master"],fighting_style="GWF",default=1)
    p2 = Character(name="Polearm + Defense",feats=["polearm_master"],fighting_style="DEFENSE",default=1)
    p3 = Character(name="GreatSword + GWF",fighting_style="GWF",weapon="2d6",default=1)
    p4 = Character(name="GreatSword + Defense",fighting_style="DEFENSE",weapon="2d6",default=1)
    p5 = Character(name="Polearm + Duelling",feats=["polearm_master"],fighting_style="DUELLING",weapon="d6",default=1)
    p6 = Character(name="Great Axe + GWF",fighting_style="GWF",weapon="d12",default=1)
    p7 = Character(name="Sword + Shield",fighting_style="DUELLING",weapon="d8",consitution=16,default=1)
    p8 = Character(name="Sword + Shield + HAM",fighting_style="DUELLING",weapon="d8",default=1,feats=["ham"])
    p9 = Character(name="Polearm + HAM + Defense",fighting_style="DEFENSE",weapon="d10",default=1,feats=["ham", "polearm_master"], strength=16)
    m = Character(monster=1)
    players = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
    stats = ["name", "ac", "weapon", "dpr", "dtpr", "ris", "eff", "dmg", "odmg"]
    headers = {}
    player_stats = []
    g_tokens = []
    for p in players:
        p_stats = {}
        for stat in stats:
            if stat in ["name", "ac", "weapon"]:
                val = "%s"%(getattr(p, stat))
            else:
                val = "%.3f"% (getattr(p, stat)(m))
            p_stats[stat] = val
            headers[stat] = max(headers.get(stat,0), len(val), len(stat))
        player_stats.append(p_stats)  
    for stat in stats:
        g_tokens.append("%s%s  " % (stat.upper()," "*(headers[stat] - len(stat))))
    g_tokens.append("\n%s%s"% ("-"*(sum(len(token) for token in g_tokens)),"\n"))
    for p_stat in sorted(player_stats, key=lambda x: float(x.get("eff")), reverse=True):
        for stat in stats:
            g_tokens.append("%s%s  " % (p_stat[stat]," "*(headers[stat] - len(p_stat[stat]))))
        g_tokens.append("\n")
    print "".join(g_tokens)


