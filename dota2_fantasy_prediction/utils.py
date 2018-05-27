import json
import requests
from db_utils import posts


def json_load(param=None):
    with open('./tmp/{}.json'.format(param), 'r') as load_f:
        ret = json.load(load_f)
    return ret


def get_match_json(match_id: int):
    ans = posts.find_one({'match_id': match_id})
    if not ans:
        ans = fetch_match_json(match_id)
        posts.insert_one(ans)
    return ans


def fetch_match_json(match_id: int):
    model = 'https://api.opendota.com/api/matches/{}'
    url = model.format(match_id)
    print("FETCHING: {}".format(url))
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.json()
