import time

from MatchHistory import Match, load_full_history
from ddragon import load_runes
from matplotlib import pyplot as plot


def create_iddict():
    data = load_runes()
    runesdict = {}
    for d in data:
        # print(d["id"], d["name"], d["slots"])
        for rset in d["slots"]:
            for r in rset["runes"]:
                runesdict[r["id"]] = r["key"]
    return runesdict


def plot_main_rune():
    matchhistory = load_full_history(update_database=True)
    iddict = create_iddict()
    runes = {}
    m: Match
    for m in matchhistory:
        for r in m.get_all_main_runes():
            if r in runes:
                runes[r] += 1
            else:
                runes[r] = 1
    runes = dict(sorted(runes.items(), reverse=True, key=lambda item: item[1]))
    xlist = []
    ylist = []
    for r in runes:
        try:
            xlist.append(iddict[r])
            ylist.append(runes[r])
        except KeyError:
            print(r)
    # xlist = ['Conqueror', 'Electrocute', 'ArcaneComet', 'DarkHarvest', 'PressTheAttack', 'Aftershock', 'LethalTempo', 'GraspOfTheUndying', 'FleetFootwork', 'SummonAery', 'HailOfBlades', 'PhaseRush', 'GlacialAugment', 'Guardian', 'Predator', 'UnsealedSpellbook', 'MasterKey']
    # ylist = [4276, 2975, 2542, 2469, 2193, 1571, 1230, 1129, 1055, 953, 516, 502, 429, 290, 121, 51, 21]

    print(iddict)
    print(xlist)
    print(ylist)
    p = plot.bar(xlist, ylist)
    plot.xticks(rotation=90)
    for rect in p:
        height = rect.get_height()
        plot.annotate('{}'.format(height),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      xytext=(0, 3),  # 3 points vertical offset
                      textcoords="offset points",
                      ha='center', va='bottom')

    plot.show()


def print_full_runepages():
    matchhistory = load_full_history(update_database=False)
    runes = {}
    m: Match
    print("Starting to analyse matches")
    for c, m in enumerate(matchhistory):
        for r in m.get_full_rune_pages(ids=False, names=True):
            string = str(r)
            if string in runes:
                runes[string] += 1
                # print("{} Runepage {} schon {}-mal vorhanden".format(c, string, runes[string]))
            else:
                # print("{} Runepage {} ist neu".format(c, string))
                runes[string] = 1
    runes = dict(sorted(runes.items(), key=lambda item: item[1], reverse=True))
    print("Done.")
    for r in runes:
        print(r, runes[r])


if __name__ == '__main__':
    t1 = time.time()
    print_full_runepages()
    t2 = time.time()
    print(t2 - t1)
