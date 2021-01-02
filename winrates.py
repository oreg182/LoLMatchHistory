from MatchHistory import Match, load_full_history
from matplotlib import pyplot as plot
import colorsys

from ddragon import load_champions


def create_champion_iddict():
    data = load_champions()
    d = {}
    for c in data:
        d[int(data[c]["key"])] = data[c]["name"]
    return d


def create_id_championdict():
    data = load_champions()
    d = {}
    for c in data:
        d[data[c]["name"]] = int(data[c]["key"])
    return d


def plot_all_winrates():
    mh = load_full_history()
    iddict = create_champion_iddict()
    reversediddict = create_id_championdict()
    winrate = {}
    for m in mh:
        win_defeat = m.win_defeat()
        for w in win_defeat[0]:
            if w in winrate:
                winrate[w][0] += 1
            else:
                winrate[w] = [1, 0]
        for l in win_defeat[1]:
            if l in winrate:
                winrate[l][1] += 1
            else:
                winrate[l] = [0, 1]
    pwinrates = {}
    for c in winrate:
        try:
            pwinrates[iddict[c]] = round(100 * (winrate[c][0] / (winrate[c][0] + winrate[c][1])), 2)
        except ZeroDivisionError:
            pwinrates[iddict[c]] = 0

    pwinrates = dict(sorted(pwinrates.items(), key=lambda item: item[1]))

    gameslist = []
    for k in pwinrates:
        gameslist.append(winrate[reversediddict[k]][0] + winrate[reversediddict[k]][1])

    p = plot.bar(pwinrates.keys(), pwinrates.values())

    r: plot.Rectangle

    games = 0
    for g in gameslist:
        games += g
    print(games)

    mingames = min(gameslist)
    maxgames = max(gameslist)

    print(mingames, maxgames)

    _range = maxgames - mingames

    for x, r in enumerate(p):
        hue = (gameslist[x]-mingames)/_range*0.3
        c = colorsys.hsv_to_rgb(hue, 1, 1)
        r.set_color(c)

    for x, rect in enumerate(p):
        height = rect.get_height()
        plot.annotate('{} {}'.format(height, gameslist[x]),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      xytext=(0, 3),  # 3 points vertical offset
                      textcoords="offset points",
                      ha='center', va='bottom', rotation=90)
    plot.xticks(rotation=90)
    plot.show()


def plot_special(queueId, patch, player=None):
    """Note patch number with ending dot; "10.1." """

    if not player:
        mh = []  # TODO filter by queue and or patch

        iddict = create_champion_iddict()
        reversediddict = create_id_championdict()
        winrate = {}
        for m in mh:
            win_defeat = m.win_defeat()
            for w in win_defeat[0]:
                if w in winrate:
                    winrate[w][0] += 1
                else:
                    winrate[w] = [1, 0]
            for l in win_defeat[1]:
                if l in winrate:
                    winrate[l][1] += 1
                else:
                    winrate[l] = [0, 1]
        print(winrate)
        pwinrates = {}
        for c in winrate:
            try:
                pwinrates[iddict[c]] = round(100 * (winrate[c][0] / (winrate[c][0] + winrate[c][1])), 2)
            except ZeroDivisionError:
                pwinrates[iddict[c]] = 0

        pwinrates = dict(sorted(pwinrates.items(), key=lambda item: item[1]))
        print(pwinrates)

        gameslist = []
        for k in pwinrates:
            gameslist.append(winrate[reversediddict[k]][0] + winrate[reversediddict[k]][1])

        p = plot.bar(pwinrates.keys(), pwinrates.values())

        for x, rect in enumerate(p):
            height = rect.get_height()
            plot.annotate('{} {}'.format(height, gameslist[x]),
                          xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', rotation=90)

        plot.xticks(rotation=90)
        plot.show()


if __name__ == '__main__':
    plot_all_winrates()
