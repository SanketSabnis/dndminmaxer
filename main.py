#!/usr/bin/python2.7
import matplotlib.pyplot as plt

import config
from player import Character


def plot_chars(players, opponents, opponent, plot_stat, plot_metric, independent_stats):
    plot_x = []
    plot_y = []
    is_level = bool(plot_metric == "level")
    for m in opponents:
        x_values = []
        y_values = []
        iterable = m if is_level else players
        for p in iterable:
            if plot_stat in independent_stats:
                val = "%s" % (getattr(p, plot_stat))
            else:
                val = (getattr(p, plot_stat)(opponent if is_level else m))
            x_values.append(getattr(p if is_level else m, plot_metric))
            y_values.append(val)
        plot_x.append(x_values)
        plot_y.append(y_values)

    xlabel = "%s %s" % ("Character" if is_level else m.char_type.title(), plot_metric.title())
    ylabel = plot_stat.upper()
    plt.plot(plot_x, plot_y, marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(
        ["%s (%.2f)" % (p.name, getattr(p, plot_stat)(opponent)) for p in players],
        loc="best"
    )


if __name__ == "__main__":
    opponent = config.opponent
    players = config.players
    independent_stats = ["name", "ac", "weapon", "strength", "dexterity", "level", "dmg_str"]
    dependent_stats = ["dpr", "eff", "ris"]
    display_stats = independent_stats[:-2] + dependent_stats + [independent_stats[-1]]
    headers = {}
    player_stats = []
    g_tokens = []
    for p in players:
        p_stats = {}
        for stat in display_stats:
            if stat in independent_stats:
                val = "%s" % (getattr(p, stat))
            else:
                val = "%.3f" % (getattr(p, stat)(opponent))
            p_stats[stat] = val
            headers[stat] = max(headers.get(stat, 0), len(val), len(stat))
        player_stats.append(p_stats)
    for stat in display_stats:
        g_tokens.append("%s%s  " % (stat.upper(), " " * (headers[stat] - len(stat))))
    g_tokens.append("\n%s%s" % ("-" * (sum(len(token) for token in g_tokens)), "\n"))
    for p_stat in sorted(player_stats, key=lambda x: float(x.get("eff", 0)), reverse=True):
        for stat in display_stats:
            g_tokens.append("%s%s  " % (p_stat[stat], " " * (headers[stat] - len(p_stat[stat]))))
        g_tokens.append("\n")
    print "".join(g_tokens)
    #
    fig = plt.figure(figsize=(15, 9), tight_layout=1)
    fignum = 221  # 2 Rows, 2 Column, 1 Figure Number
    for plot_metric in ["ac", "level"]:
        if plot_metric == "ac":
            monsters = [Character(**{"char_type": opponent.char_type, plot_metric: metric_value})
                        for metric_value in range(20, 9, -1)]
        else:
            monsters = [
                [Character(**dict(p.init_params, **{plot_metric: metric_value})) for p in players]
                for metric_value in range(1, 14)
            ]
        for plot_stat in ["eff", "dpr"]:
            plt.subplot(fignum)
            fignum += 1
            plot_chars(players, monsters, opponent, plot_stat, plot_metric, independent_stats)

    plt.show()
