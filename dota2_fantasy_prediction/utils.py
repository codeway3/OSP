import json
import requests
from db_utils import posts


def json_load(param=None):
    with open('./tmp/{}.json'.format(param), 'r') as load_f:
        ret = json.load(load_f)
    return ret


def get_match_json(match_id: int, show_log=True):
    db_has_data = True
    ans = posts.find_one({'match_id': match_id})
    if not ans:
        db_has_data = False
        ans = fetch_match_json(match_id, show_log)
        posts.insert_one(ans)
    return db_has_data, ans


def fetch_match_json(match_id: int, show_log=True):
    model = 'https://api.opendota.com/api/matches/{}'
    url = model.format(match_id)
    if show_log:
        print("FETCHING: {}".format(url))
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.json()


def fetch_league_json(id, url):
    print("FETCHING LEAGUE {}".format(id))
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.json()
