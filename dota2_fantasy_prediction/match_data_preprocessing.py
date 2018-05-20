from json_load import json_load
from player_fantasy_calc import player_fantasy_calc


def unknown_function():
    init_dict = json_load('3870838763')
    fin_dict = {}
    fin_dict['radiant_team'] = init_dict['radiant_team']
    fin_dict['dire_team'] = init_dict['dire_team']
    fin_dict['players'] = []
    for tmp_dict in init_dict['players']:
        fin_dict['players'].append(player_fantasy_calc(tmp_dict))
    return fin_dict


if __name__ == '__main__':
    ans = unknown_function()
    print(ans)
