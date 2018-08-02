from ..utils import get_match_json, json_load


calculation_rules = {
    'kills': 0.3,
    'deaths': -0.3,
    'assists': 0.15,
    'last_hits': 0.003,
    'gold_per_min': 0.002,
    'tower_kills': 1,
    'roshan_kills': 1,
    'teamfight_participation': 3,
    'observer_uses': 0.5,
    'camps_stacked': 0.5,
    'rune_pickups': 0.25,
    'firstblood_claimed': 4.0,
    'stuns': 0.05
}


def calc_player_fantasy(init_dict: dict=None):
    if not init_dict:
        init_dict = json_load('player')
    keys = ['kills', 'deaths', 'assists', 'last_hits', 'gold_per_min', 'tower_kills', 'roshan_kills', 'teamfight_participation', 'observer_uses', 'camps_stacked', 'rune_pickups', 'firstblood_claimed', 'stuns']
    fin_dict = {}
    for key in keys:
        try:
            fin_dict[key] = round(init_dict[key] * calculation_rules[key], 2)
        except Exception as e:
            print('Exception {} happened around {}'.format(e, key))
    fin_dict['sum'] = round(sum(fin_dict[key] for key in keys), 2)
    fin_dict['name'] = init_dict['name']
    return fin_dict


def calc_match_fantasy(match_id: int=None):
    if not match_id:
        _, init_dict = get_match_json(3870838763)
    else:
        _, init_dict = get_match_json(match_id)
    fin_dict = {}
    fin_dict['radiant_team'] = init_dict['radiant_team']
    fin_dict['dire_team'] = init_dict['dire_team']
    fin_dict['players'] = []
    for player_dict in init_dict['players']:
        fin_dict['players'].append(calc_player_fantasy(player_dict))
    return fin_dict
