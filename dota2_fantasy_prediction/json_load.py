import json


def json_load(param=None):
    with open('./tmp/{}.json'.format(param), 'r') as load_f:
        ret = json.load(load_f)
    return ret
