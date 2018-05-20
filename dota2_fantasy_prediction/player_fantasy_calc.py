from json_load import json_load
from calculation_rules import calculation_rules as cal


def player_fantasy_calc(init_dict=None):
    if not init_dict:
        init_dict = json_load('player')
    keys = ['kills', 'deaths', 'assists', 'last_hits', 'gold_per_min', 'tower_kills', 'roshan_kills', 'teamfight_participation', 'observer_uses', 'camps_stacked', 'rune_pickups', 'firstblood_claimed', 'stuns']
    fin_dict = {}
    for key in keys:
        try:
            fin_dict[key] = init_dict[key] * cal[key]
        except Exception as e:
            print('Exception {} happened around {}'.format(e, key))
    fin_dict['sum'] = sum(fin_dict[key] for key in keys)
    fin_dict['name'] = init_dict['name']
    return fin_dict


if __name__ == "__main__":
    ans = player_fantasy_calc()
    print(ans)
