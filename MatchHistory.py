import time

import cassiopeia as cass
import json
import requests
import datetime
import sqlite3
import ast

TOKEN = 0
if not TOKEN:
    TOKEN = input("Missing RiotAPIToken: ")
cass.set_riot_api_key(TOKEN)


def load_full_history(summoner="oreg182", region="EUW", update_database=False):
    print("loading full history...")
    if update_database:
        update_match_history(summoner, region)
    simple_match_history = open_match_history(summoner)
    match_history = []
    for m in simple_match_history:
        match_history.append(Match(m["id"]))
    print("Done.")
    return match_history


def update_match_history(summoner, region):
    with open("matchhistory_" + summoner + ".json", "w") as f:
        s = cass.Summoner(name=summoner, region=region)
        mh = s.match_history
        mhlist = []
        m: cass.Match
        for m in mh:
            m2 = m.to_dict()
            m2["creation"] = m2["creation"].strftime("%d/%m/%Y, %H:%M:%S")
            mhlist.append(m2)
            print(m2)
        json.dump(mhlist, f, indent=4)


class Match:
    def __init__(self, matchid=4797414895, conn=sqlite3.connect("full_match_database.db")):

        self.gameId: int = matchid
        self.conn = conn

        self.data = {}

        self.check_in_database()

        self.platformId: str = self.data["platformId"]
        self.gameCreation: int = self.data["gameCreation"]
        self.gameDuration: int = self.data["gameDuration"]
        self.queueId: int = self.data["queueId"]
        self.mapId: int = self.data["mapId"]
        self.seasonId: int = self.data["seasonId"]
        self.gameVersion: str = self.data["gameVersion"]
        self.gameMode: str = self.data["gameMode"]
        self.gameType: str = self.data["gameType"]
        self.teams: list = self.data["teams"]
        self.participants = self.data["participants"]
        self.participantIdentities: list = self.data["participantIdentities"]

    def get_all_champions(self):
        champs = []
        for p in self.participants:
            champs.append(p["championId"])
        return champs

    def get_all_summoner(self):
        summ = []
        for summoner in self.participantIdentities:
            summ.append(summoner["player"]["summonerName"])
        return summ

    def get_all_main_runes(self):
        runes = []
        for p in self.participants:
            try:
                runes.append(p["perk0"])
            except KeyError:
                print("NO MAIN RUNE", p)
        return runes

    def get_full_rune_pages(self, ids=True, names=False):
        from plotRunesFrequency import create_iddict
        runes = []
        iddict = create_iddict()
        for p in self.participants:
            try:
                p = p["stats"]
                runes.append([[p["perk0"], p["perk1"], p["perk2"], p["perk3"]], [p["perk4"], p["perk5"]]])
            except KeyError:
                print("No Runes Found in Match {}".format(self.gameId))
                return []
        runenames = []
        for p in runes:
            runenames.append([])
            for l in p:
                runenames[-1].append([])
                for r in l:
                    try:
                        runenames[-1][-1].append(iddict[r])
                    except KeyError:
                        print("no fitting rune with id {}".format(r))
        if ids:
            return runes
        elif ids and names:
            return runes, runenames
        else:
            return runenames

    def check_in_database(self):
        s = "select * from matches where gameId = {}".format(self.gameId)
        data = select_special(s)
        if data:
            #  print("data exists in database: match {}".format(self.gameId))
            self.data = data[0]
        else:
            region = "euw1"  # change if necessary
            print("trying request match {}".format(self.gameId))
            data = requests.get("https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(self.gameId),
                                headers={"X-Riot-Token": TOKEN})
            print("received {}".format(data.text))
            self.data = json.loads(data.text)
            time.sleep(1.2)
            insert_match(self.data, self.conn)

    def win_defeat(self):
        """:returns list, list"""
        win = []
        defeat = []
        for p in self.participants:
            if p["stats"]["win"]:
                win.append(p["championId"])
            else:
                defeat.append(p["championId"])
        return win, defeat

    def __str__(self):
        string = """
        === MATCH {id} === {time} ===
        {queue}
        BLUE TEAM:
        
        RED TEAM:
        
        =============================
        """.format(id=self.gameId,
                   time=datetime.datetime.fromtimestamp(self.gameCreation).strftime("%d/%m/%Y, %H:%M:%S"),
                   queue=self.queueId)
        return string


def open_match_history(summoner="oreg182"):
    with open("matchhistory_" + summoner + ".json") as f:
        match_history = json.load(f)
    return match_history


def insert_match(data, conn):
    insertstring = """insert into matches
    (gameId, queueId, gameType, gameDuration, platformId, gameCreation, seasonId, gameVersion, mapId, gameMode, teams, participants, participantIdentities) values
    (?,?,?,?,?,?,?,?,?,?,?,?,?);
    """

    gameId = data["gameId"]
    platformId = data["platformId"]
    gameCreation = data["gameCreation"]
    gameDuration = data["gameDuration"]
    queueId = data["queueId"]
    mapId = data["mapId"]
    seasonId = data["seasonId"]
    gameVersion = data["gameVersion"]
    gameMode = data["gameMode"]
    gameType = data["gameType"]
    teams = str(data["teams"])
    participants = str(data["participants"])
    participantIdentities = str(data["participantIdentities"])

    values = (
        gameId, queueId, gameType, gameDuration, platformId, gameCreation, seasonId, gameVersion, mapId, gameMode,
        teams,
        participants, participantIdentities)  # replaces the questionmarks in insertstring

    cursor = conn.cursor()
    cursor.execute(insertstring, values)
    conn.commit()


def select_special(statement, conn=sqlite3.connect("full_match_database.db")):
    # auto convert to json

    keys = ["gameId", "queueId", "gameType", "gameDuration", "platformId", "seasonId", "gameVersion", "mapId",
            "gameMode", "teams", "participants", "participantIdentities", "gameCreation"]

    c = conn.cursor()
    l = []
    for line in c.execute(statement):
        z = zip(keys, line)
        d = dict(z)
        d["teams"] = ast.literal_eval(d["teams"])
        d["participants"] = ast.literal_eval(d["participants"])
        d["participantIdentities"] = ast.literal_eval(d["participantIdentities"])
        l.append(d)
    return l


def select_all():
    conn = sqlite3.connect("full_match_database.db")
    c = conn.cursor()
    c.execute("select * from matches")
    l = []
    for i in c.execute("select * from matches"):
        print(i)
        l.append(i)
    return l


def download_missing():
    update_match_history("oreg182", "EUW")
    match_history = open_match_history()
    conn = sqlite3.connect("full_match_database.db")
    for i, m in enumerate(match_history):
        print(i)
        Match(m["id"], conn)


def format_runes(matchid):
    for p in Match(matchid).get_full_rune_pages(ids=False, names=True):
        print(p)


if __name__ == '__main__':
    Match().winrate()
