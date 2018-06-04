from ..utils import get_match_json, json_load
from .calc_player_fantasy import calc_player_fantasy


def calc_match_fantasy(match_id: int=None):
    if not match_id:
        init_dict = json_load(3870838763)
    else:
        _, init_dict = get_match_json(match_id)
    fin_dict = {}
    fin_dict['radiant_team'] = init_dict['radiant_team']
    fin_dict['dire_team'] = init_dict['dire_team']
    fin_dict['players'] = []
    for player_dict in init_dict['players']:
        fin_dict['players'].append(calc_player_fantasy(player_dict))
    return fin_dict


if __name__ == '__main__':
    ans = calc_match_fantasy(3870838763)
    print(ans)
