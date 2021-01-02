import json

import requests


def download_file(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def check_latest_version():
    latest = json.loads(requests.get("https://ddragon.leagueoflegends.com/api/versions.json").text)[0]
    return latest


def load_champions():
    data = json.loads(requests.get(
        "http://ddragon.leagueoflegends.com/cdn/" + check_latest_version() + "/data/en_US/champion.json").text)
    return data["data"]


def load_runes():
    data = json.loads(requests.get(
        "http://ddragon.leagueoflegends.com/cdn/" + check_latest_version() + "/data/en_US/runesReforged.json").text)
    return list(data)


if __name__ == '__main__':
    load_champions()
