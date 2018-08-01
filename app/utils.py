import json
import requests
from pymongo import MongoClient
from . import app


logger = app.logger

client = MongoClient()
db = client['matches']
posts = db.posts


def json_load(param: str=None):
    with open('./tmp/{}.json'.format(param), 'r') as load_f:
        ret = json.load(load_f)
    return ret


def fetch_json(url: str, show_log: bool=True):
    if show_log:
        logger.debug("FETCHING: {}".format(url))
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
    try:
        response = requests.get(url)
        logger.debug(response)
    except:
        logger.error()
        exit()
    if response.status_code == requests.codes.ok:
        return response.json()


def get_match_json(match_id: int):
    db_has_data = True
    ans = posts.find_one({'match_id': match_id})
    if not ans:
        db_has_data = False
        ans = fetch_match_json(match_id, )
        posts.insert_one(ans)
    return db_has_data, ans


def fetch_match_json(match_id: int):
    model = 'https://api.opendota.com/api/matches/{}'
    url = model.format(match_id)
    return fetch_json(url)


def fetch_league_json(league_id: int, url: str):
    logger.debug("FETCHING LEAGUE {}".format(league_id))
    return fetch_json(url, show_log=False)


def fetch_player_matches_json(player_id: int):
    model = 'https://api.opendota.com/api/players/{}/matches'
    url = model.format(player_id)
    return fetch_json(url)
