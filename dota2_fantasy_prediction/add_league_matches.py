import sys
import time
import click
from utils import fetch_league_json, get_match_json


url_model = 'https://api.opendota.com/api/explorer?sql=SELECT%0Amatches.match_id%20%2C%0Aavg(1)%20avg%2C%0Acount(distinct%20matches.match_id)%20count%2C%0Asum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1)%20winrate%2C%0A((sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1))%20%0A%20%20%2B%201.96%20*%201.96%20%2F%20(2%20*%20count(1))%20%0A%20%20-%201.96%20*%20sqrt((((sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1))%20*%20(1%20-%20(sum(case%20when%20(player_matches.player_slot%20%3C%20128)%20%3D%20radiant_win%20then%201%20else%200%20end)%3A%3Afloat%2Fcount(1)))%20%2B%201.96%20*%201.96%20%2F%20(4%20*%20count(1)))%20%2F%20count(1))))%0A%20%20%2F%20(1%20%2B%201.96%20*%201.96%20%2F%20count(1))%20winrate_wilson%2C%0Asum(1)%20sum%2C%0Amin(1)%20min%2C%0Amax(1)%20max%2C%0Astddev(1%3A%3Anumeric)%20stddev%0AFROM%20matches%0AJOIN%20match_patch%20using(match_id)%0AJOIN%20leagues%20using(leagueid)%0AJOIN%20player_matches%20using(match_id)%0AJOIN%20heroes%20on%20heroes.id%20%3D%20player_matches.hero_id%0ALEFT%20JOIN%20notable_players%20ON%20notable_players.account_id%20%3D%20player_matches.account_id%20AND%20notable_players.locked_until%20%3D%20(SELECT%20MAX(locked_until)%20FROM%20notable_players)%0ALEFT%20JOIN%20teams%20using(team_id)%0AWHERE%20TRUE%0AAND%20matches.leagueid%20%3D%20{}%0AGROUP%20BY%20matches.match_id%0AHAVING%20count(distinct%20matches.match_id)%20%3E%3D%201%0AORDER%20BY%20avg%20DESC%2Ccount%20DESC%20NULLS%20LAST%0ALIMIT%201000'


def progress(count, total, title=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + ' ' * (bar_len - filled_len)

    sys.stdout.write('\r{}[{}] {}{}'.format(title, bar, percents, '%'))
    sys.stdout.flush()


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


@click.command()
@click.option('--lid', default=9880, help='ID of league.')
def cli(lid):
    add_league_matches(league_id=lid, have_progress=True)


if __name__ == '__main__':
    cli()
