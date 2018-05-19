import json
from calculation_rules import cal_rules as cal

with open('./tmp/player.json', 'r') as load_f:
    init_dict = json.load(load_f)

keys = ['kills', 'deaths', 'assists', 'last_hits', 'gold_per_min', 'tower_kills', 'roshan_kills', 'teamfight_participation', 'observer_uses', 'camps_stacked', 'rune_pickups', 'firstblood_claimed', 'stuns']
fin_dict = {}
for key in keys:
    try:
        fin_dict[key] = init_dict[key] * cal[key]
    except Exception as e:
        print('Exception {} happened around {}'.format(key))
fin_dict['sum'] = sum(fin_dict[key] for key in keys)

print(fin_dict)
