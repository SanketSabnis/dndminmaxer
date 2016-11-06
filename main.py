#!/usr/bin/python2.7
import os
import sys
from config import *
from evaluator import *
from player import Character
import matplotlib.pyplot as plt

def plot_chars(players, stat, metric, metric_range):
    plot_x = []
    plot_y = []
    count = 0
    monsters = [Character(**{"char_type": "monster", metric: metric_value}) for metric_value in metric_range]
    for m in monsters:
        x_values = []
        y_values = []
        for p in players:
            if stat in ["name", "ac", "weapon", "dmg_str", "strength"]:
                val = "%s"%(getattr(p, stat))
            else:
                val = (getattr(p, stat)(m))
            setattr(p, "legend_stat", val)
            x_values.append(getattr(m, metric))
            y_values.append(val)
        plot_x.append(x_values)
        plot_y.append(y_values)

    plt.plot(plot_x, plot_y, antialiased=True, marker="o")
    plt.xlabel("Monster %s"%metric.upper())
    plt.ylabel(stat.upper())
    plt.legend(["%s (%.2f)" % (p.name, p.legend_stat) for p in players])
    plt.show()



if __name__ == "__main__":
    #print evaluate("(d6)")
    #sys.exit(0)
    #p0 = Character(name="Polearm + GWF",feats=["polearm_master"],fighting_style="GWF",default=1)
    #p1 = Character(name="Polearm + GWF + SOF",feats=["polearm_master"],fighting_style="GWF",default=1, shield=2)
    #p2 = Character(name="Polearm + GWF + Smite",feats=["polearm_master"],fighting_style="GWF",default=1, smite="+d8")
    #p3 = Character(name="Polearm + GWF + Bless",feats=["polearm_master"],fighting_style="GWF",default=1, bless="d4")
    #p4 = Character(name="Polearm + GWF + Hunter",feats=["polearm_master"],fighting_style="GWF",default=1, weapon="d10+d6")
    #p5  = Character(name="Archer", feats=["gwm"], fighting_style="ARCHERY", char_type="paladin")
    p6  = Character(name="GWM", feats=["gwm"], fighting_style="GWF", char_type="paladin", weapon="2d6")
    p7  = Character(name="Archery",feats=["gwm", "xbow_expert"], fighting_style="ARCHERY",char_type="paladin", attack_att="dex_mod", dexterity=16, strength=8, weapon="d6", attacks=1)
    p8  = Character(name="Polearm Master", feats=["polearm_master"], fighting_style="GWF", char_type="paladin")#, modifiers=["adv", "bless", "hunter"])
    #p9  = Character(name="GWF+ADV+Bless+Hunter+Smite+Haste",feats=["polearm_master"], fighting_style="GWF", char_type="paladin", modifiers=["adv", "bless", "haste", "smite"])
    #p8  = Character(name="GWF+ADV+BLESS+Hunter+Smite+Haste",feats=["polearm_master"],fighting_style="GWF",default=1,  bless="d4")
    m = Character(char_type="monster", ac=14)
    players = [p6, p7, p8]
    stats = ["name", "dpr", "eff", "ris", "dmg_str"]
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
    #plot_chars(players, "eff", "attacks", range(1, 8))
