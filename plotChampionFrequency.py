from MatchHistory import load_full_history, Match
import matplotlib.pyplot as plot
from ddragon import load_champions


def create_champion_iddict():
    data = load_champions()
    d = {}
    for c in data:
        d[int(data[c]["key"])] = data[c]["name"]
    return d


def plot_all_matches(summoner="oreg182", region="EUW"):
    champs = {}
    iddict = create_champion_iddict()
    matchhistory = load_full_history(summoner, region)
    m: Match
    for m in matchhistory:
        champs_in_match = m.get_all_champions()
        for c in champs_in_match:
            if iddict[c] in champs:
                champs[iddict[c]] += 1
            else:
                champs[iddict[c]] = 1
    champs = dict(sorted(champs.items(), key=lambda item: item[1]))
    print(champs)
    plot.bar(champs.keys(), champs.values())
    plot.xticks(rotation=90)
    plot.rc('xtick', labelsize=8)
    plot.show()


if __name__ == '__main__':
    champs = {'Rell': 2, 'Aurelion Sol': 21, 'Skarner': 23, 'Ivern': 23, 'Taliyah': 29, 'Seraphine': 30, 'Elise': 35, "Rek'Sai": 35, 'Kled': 40, 'Udyr': 44, 'Yorick': 44, 'Rammus': 45, 'Corki': 45, 'Viktor': 46, 'Gnar': 47, 'Taric': 49, 'Tahm Kench': 50, 'Rumble': 50, 'Sion': 51, 'Xin Zhao': 53, 'Kennen': 54, 'Trundle': 54, 'Jayce': 55, 'Lissandra': 58, 'Zac': 60, 'Poppy': 65, 'Kalista': 67, "Kog'Maw": 68, 'Braum': 68, 'Gangplank': 70, 'Alistar': 73, 'Jarvan IV': 73, 'Anivia': 74, 'Gragas': 74, 'Azir': 74, 'Malzahar': 76, 'Camille': 77, 'Zilean': 77, 'Bard': 80, 'Samira': 81, 'Kindred': 82, 'Singed': 84, 'Qiyana': 86, 'Nunu & Willump': 86, 'Olaf': 86, 'Maokai': 87, 'Illaoi': 88, 'Orianna': 89, 'Hecarim': 90, 'Lillia': 91, 'Yone': 93, 'Cassiopeia': 93, 'Rengar': 94, 'Ornn': 96, 'Dr. Mundo': 96, 'Heimerdinger': 97, 'Ziggs': 97, 'Zyra': 98, 'Wukong': 98, 'Nami': 98, 'Rakan': 98, 'Evelynn': 98, 'Quinn': 100, 'Janna': 103, 'Vi': 104, 'Shen': 104, 'Karthus': 106, 'Nidalee': 107, 'Shyvana': 108, 'Kassadin': 109, 'Karma': 109, 'Twisted Fate': 111, 'Tryndamere': 111, 'Graves': 112, 'Amumu': 113, 'Fiora': 116, 'Aphelios': 118, 'Lulu': 119, 'Urgot': 120, 'Xerath': 121, 'Pantheon': 122, 'LeBlanc': 123, 'Neeko': 123, 'Riven': 123, 'Shaco': 124, 'Galio': 124, 'Fiddlesticks': 125, 'Sejuani': 125, 'Swain': 125, 'Vladimir': 126, "Cho'Gath": 130, 'Sona': 130, 'Sivir': 133, 'Irelia': 134, 'Kayle': 135, 'Varus': 136, 'Xayah': 136, 'Ryze': 137, 'Diana': 138, 'Renekton': 138, 'Draven': 139, 'Aatrox': 141, 'Syndra': 146, 'Talon': 147, 'Annie': 148, 'Nasus': 149, 'Zoe': 154, 'Fizz': 155, 'Soraka': 164, 'Sylas': 165, 'Warwick': 167, 'Twitch': 169, 'Yuumi': 170, "Kha'Zix": 184, 'Jax': 184, 'Lucian': 187, 'Blitzcrank': 187, "Vel'Koz": 188, 'Leona': 189, 'Katarina': 192, 'Ekko': 211, 'Lee Sin': 214, 'Nocturne': 218, 'Darius': 223, 'Brand': 226, 'Sett': 228, 'Akali': 230, 'Jinx': 230, 'Nautilus': 231, "Kai'Sa": 232, 'Mordekaiser': 233, 'Ahri': 238, 'Vayne': 239, 'Zed': 242, 'Tristana': 249, 'Teemo': 253, 'Pyke': 258, 'Malphite': 265, 'Thresh': 275, 'Garen': 281, 'Kayn': 282, 'Morgana': 286, 'Volibear': 299, 'Senna': 302, 'Veigar': 318, 'Master Yi': 333, 'Ezreal': 335, 'Miss Fortune': 361, 'Ashe': 363, 'Jhin': 368, 'Yasuo': 382, 'Lux': 436, 'Caitlyn': 472}
    plot.bar(champs.keys(), champs.values())
    plot.xticks(rotation=90, size=7)
    plot.show()
