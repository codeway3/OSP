import sys
import time
import json
import requests
from pymongo import MongoClient
from . import app


logger = app.logger

client = MongoClient()
posts = client['matches'].posts
heatmap = client['heatmap'].posts
teams = client['teams'].posts
ti8_teams = client['teams'].ti8

timeout = 86400


url_model = 'https://api.opendota.com/api/explorer?sql=SELECT%0Amatches.match_id%20%2C%0Aavg(1)%20avg%2C%0Acount(distinct%20matches.match_id)%20count%2C%0Asum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1)%20winrate%2C%0A((sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1))%20%0A%20%20%2B%201.96%20*%201.96%20%2F%20(2%20*%20count(1))%20%0A%20%20-%201.96%20*%20sqrt((((sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1))%20*%20(1%20-%20(sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1)))%20%2B%201.96%20*%201.96%20%2F%20(4%20*%20count(1)))%20%2F%20count(1))))%0A%20%20%2F%20(1%20%2B%201.96%20*%201.96%20%2F%20count(1))%20winrate_wilson%2C%0Asum(1)%20sum%2C%0Amin(1)%20min%2C%0Amax(1)%20max%2C%0Astddev(1%3A%3Anumeric)%20stddev%0AFROM%20matches%0AJOIN%20match_patch%20using(match_id)%0AJOIN%20leagues%20using(leagueid)%0AJOIN%20player_matches%20using(match_id)%0AJOIN%20heroes%20on%20heroes.id%20%3D%20player_matches.hero_id%0ALEFT%20JOIN%20notable_players%20ON%20notable_players.account_id%20%3D%20player_matches.account_id%20AND%20notable_players.locked_until%20%3D%20(SELECT%20MAX(locked_until)%20FROM%20notable_players)%0ALEFT%20JOIN%20teams%20using(team_id)%0AWHERE%20TRUE%0AAND%20matches.leagueid%20%3D%20{}%0AGROUP%20BY%20matches.match_id%0AHAVING%20count(distinct%20matches.match_id)%20%3E%3D%201%0AORDER%20BY%20avg%20DESC%2Ccount%20DESC%20NULLS%20LAST%0ALIMIT%201000'


def progress(count, total, title=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + ' ' * (bar_len - filled_len)

    sys.stdout.write('\r{}[{}] {}{}'.format(title, bar, percents, '%'))
    sys.stdout.flush()


def team_upsert(db, info: dict):
    db.update({'team_id': info['team_id']}, {'$set': info}, upsert=True)


def add_league_matches(league_id, have_progress=False):
    url = url_model.format(league_id)
    init_dict = fetch_league_json(league_id, url)
    num = 0
    total = init_dict['rowCount']
    rows = init_dict['rows']
    print('matches count: {}'.format(total))
    try:
        for row in rows:
            num += 1
            match_id = row['match_id']
            db_has_data, _ = get_match_json(match_id, show_log=False)
            if not db_has_data:
                time.sleep(1.2)
            if have_progress:
                progress(num, total)
    except Exception as e:
        print(e)
        print("Exception occurred and rerun.")
        add_league_matches(league_id, have_progress)


def fetch_league_json(league_id: int, url: str):
    logger.debug("FETCHING LEAGUE {}".format(league_id))
    return fetch_json(url, show_log=False)


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
    except Exception as e:
        logger.error(e)
        exit()
    if response.status_code == requests.codes.ok:
        return response.json()


def get_match_json(match_id: int):
    try:
        db_has_data = True
        ans = posts.find_one({'match_id': match_id})
        if not ans:
            db_has_data = False
            ans = fetch_match_json(match_id)
            posts.insert_one(ans)
            # upsert team infomation
            info = ans['radiant_team']
            team_upsert(db=teams, info=info)
            info = ans['dire_team']
            team_upsert(db=teams, info=info)
        return db_has_data, ans
    except Exception:
        logger.error('MongoDB error!')


def fetch_match_json(match_id: int):
    model = 'https://api.opendota.com/api/matches/{}'
    url = model.format(match_id)
    return fetch_json(url)


def get_player_matches_json(player_id: int):
    now_ticks = time.time()
    try:
        ans = heatmap.find_one({'player_id': player_id})
        if not ans or now_ticks - ans['ticks'] > timeout:
            ans = {}
            ans['player_id'] = player_id
            ans['ticks'] = now_ticks
            ans['json'] = fetch_player_matches_json(player_id)
            heatmap.insert_one(ans)
        return ans['json']
    except Exception:
        logger.error('MongoDB error!')


def fetch_player_matches_json(player_id: int):
    model = 'https://api.opendota.com/api/players/{}/matches'
    url = model.format(player_id)
    return fetch_json(url)


# tmp function
def tmp_add_team_info():
    # p = posts.find()
    # cnt = p.count()
    # for i, post in enumerate(p):
    #     info = post['radiant_team']
    #     team_upsert(db=teams, info=info)
    #     info = post['dire_team']
    #     team_upsert(db=teams, info=info)
    #     progress(i+1, cnt)
    # pass
    # ti8teams = json_load('ti8_teams')['ti8teams']
    # for team in teams.find():
    #     if team['tag'] in ti8teams:
    #         team_upsert(db=ti8_teams, info=team)
    #         print(team['tag'])
    #     else:
    #         print(team['tag'], end=' ')
    # print()
    # print(ti8_teams.count())
    pass
