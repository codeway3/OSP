import requests


def get_match_api_json(match_id):
    model = 'https://api.opendota.com/api/matches/{}'
    url = model.format(match_id)
    print(url)
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.json()
