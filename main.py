#!/usr/bin/python2.7
import os
import sys
from config import *
from player import Character
import matplotlib.pyplot as plt

def plot_chars(players, stat, metric, metric_range):
    plot_x = []
    plot_y = []
    count = 0
    monsters = [Character(**{"monster":1, metric: metric_value}) for metric_value in metric_range]
    for m in monsters:
        x_values = []
        y_values = []
        for p in players:
            if stat in ["name", "ac", "weapon", "dmg_str", "strength"]:
                val = "%s"%(getattr(p, stat))
            else:
                val = (getattr(p, stat)(m))
            x_values.append(getattr(m, metric))
            y_values.append(val)
        plot_x.append(x_values)
        plot_y.append(y_values)

    plt.plot(plot_x, plot_y, antialiased=True, marker="o")
    plt.xlabel("Monster AC")
    plt.ylabel(stat.upper())
    plt.legend([p.name for p in players])
    plt.show()



if __name__ == "__main__":
    #print evaluate("(d4)")
    #sys.exit(0)
    p1 = Character(name="Polearm + GWF",feats=["polearm_master"],fighting_style="GWF",default=1)
    p2 = Character(name="Polearm + Defense",feats=["polearm_master"],fighting_style="DEFENSE",default=1)
    p3 = Character(name="GreatSword + GWF + GWM",fighting_style="GWF",weapon="2d6",default=1,feats=["gwm"])
    p4 = Character(name="Polearm + Duelling",feats=["polearm_master"],fighting_style="DUELLING",weapon="d6",default=1)
    p5 = Character(name="SnB + Duelling",fighting_style="DUELLING",weapon="d8",consitution=16,default=1)
    p6 = Character(name="SnB + HAM + Duelling",fighting_style="DUELLING",weapon="d8",default=1,feats=["ham"])
    p7 = Character(name="Polearm + HAM + Defense",fighting_style="DEFENSE",weapon="d10",default=1,feats=["ham", "polearm_master"])
    p8 = Character(name="Polearm + Savage + Defense",fighting_style="DEFENSE",weapon="d10",default=1,feats=["savage", "polearm_master"])
    p9 = Character(name="Polearm + Savage + GWF",fighting_style="GWF",weapon="d10",default=1,feats=["savage", "polearm_master"])
    p10 = Character(name="SnB + HAM + Savage + Duelling",fighting_style="DUELLING",weapon="d8",default=1,feats=["ham", "savage"])
    p11 = Character(name="Polearm + GWM + Defense",feats=["polearm_master","gwm"],fighting_style="DEFENSE",default=1)
    p12 = Character(name="Polearm + GWM + GWF",feats=["polearm_master","gwm"],fighting_style="GWF",default=1)
    m = Character(monster=1, ac=14)
    players = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
    stats = ["name", "ac", "weapon", "strength", "dpr", "dtpr", "ris", "eff", "dmg", "dmg_str"]
    headers = {}
    player_stats = []
    g_tokens = []
    for p in players:
        p_stats = {}
        for stat in stats:
            if stat in ["name", "ac", "weapon", "dmg_str", "strength"]:
                val = "%s"%(getattr(p, stat))
            else:
                val = "%.3f"% (getattr(p, stat)(m))
            p_stats[stat] = val
            headers[stat] = max(headers.get(stat,0), len(val), len(stat))
        player_stats.append(p_stats)  
    for stat in stats:
        g_tokens.append("%s%s  " % (stat.upper()," "*(headers[stat] - len(stat))))
    g_tokens.append("\n%s%s"% ("-"*(sum(len(token) for token in g_tokens)),"\n"))
    for p_stat in sorted(player_stats, key=lambda x: float(x.get("eff",0)), reverse=True):
        for stat in stats:
            g_tokens.append("%s%s  " % (p_stat[stat]," "*(headers[stat] - len(p_stat[stat]))))
        g_tokens.append("\n")
    print "".join(g_tokens)
    plot_chars(players, "eff", "ac", range(20, 10, -1))
