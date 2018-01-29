#!/usr/bin/python2.7
from player import Character
import matplotlib.pyplot as plt


def plot_chars(players, stat, metric, metric_range):
    plot_x = []
    plot_y = []
    monsters = [Character(**{"char_type": "monster", metric: metric_value})
                for metric_value in metric_range]
    lm = monsters[6]
    for m in monsters:
        x_values = []
        y_values = []
        for p in players:
            if stat in ["name", "ac", "weapon", "dmg_str", "strength"]:
                val = "%s" % (getattr(p, stat))
            else:
                val = (getattr(p, stat)(m))
            setattr(p, "legend_stat", val)
            x_values.append(getattr(m, metric))
            y_values.append(val)
        plot_x.append(x_values)
        plot_y.append(y_values)

    plt.plot(plot_x, plot_y, marker="o")
    plt.xlabel("Monster %s" % metric.upper())
    plt.ylabel(stat.upper())
    plt.legend(["%s (%.2f)" % (p.name, getattr(p, stat)(lm)) for p in players])
    plt.show()


if __name__ == "__main__":
    # print evaluate("(d6)")
    # sys.exit(0)
    p0 = Character(name="Great Sword GWM", feats=["gwm"], char_type="fighter", fighting_style="GWF",
                   weapon="2d6")
    p1 = Character(name="Great Axe GWM", feats=["gwm"], char_type="fighter", fighting_style="GWF",
                   weapon="d12")
    p2 = Character(name="SnB HAM", feats=["ham"], fighting_style="DUELLING", char_type="fighter",
                   weapon="d8", )
    p3 = Character(name="Archery SS", feats=["xbow_expert", "gwm"],
                   fighting_style="ARCHERY", char_type="fighter", attack_att="dex_mod",
                   dexterity=16, ac=16, weapon="d6")
    p4 = Character(name="Great Sword GWM2", feats=["gwm2"], char_type="fighter",
                   fighting_style="GWF", weapon="2d6")
    p5 = Character(name="Great Axe GWM2", feats=["gwm2"], char_type="fighter", fighting_style="GWF",
                   weapon="d12")
    p6 = Character(name="Archery Xbow SS2", feats=["xbow_expert", "gwm2"],
                   fighting_style="ARCHERY", char_type="fighter", attack_att="dex_mod",
                   dexterity=16, ac=16, weapon="d6")
    m = Character(char_type="monster")
    players = [p0, p1, p2, p3, p4, p5, p6]
    stats = ["name", "ac", "strength", "dexterity", "dpr", "eff", "ris", "dmg_str"]
    headers = {}
    player_stats = []
    g_tokens = []
    for p in players:
        p_stats = {}
        for stat in stats:
            if stat in ["name", "ac", "weapon", "dmg_str", "strength", "dexterity"]:
                val = "%s" % (getattr(p, stat))
            else:
                val = "%.3f" % (getattr(p, stat)(m))
            p_stats[stat] = val
            headers[stat] = max(headers.get(stat, 0), len(val), len(stat))
        player_stats.append(p_stats)
    for stat in stats:
        g_tokens.append("%s%s  " % (stat.upper(), " " * (headers[stat] - len(stat))))
    g_tokens.append("\n%s%s" % ("-" * (sum(len(token) for token in g_tokens)), "\n"))
    for p_stat in sorted(player_stats, key=lambda x: float(x.get("eff", 0)), reverse=True):
        for stat in stats:
            g_tokens.append("%s%s  " % (p_stat[stat], " " * (headers[stat] - len(p_stat[stat]))))
        g_tokens.append("\n")
    print "".join(g_tokens)
    plot_chars(players, "eff", "ac", range(20, 10, -1))
