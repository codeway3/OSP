import sys
import click
sys.path.append('..')
from OSP.dota2_fantasy_prediction import add_league_matches, calc_match_fantasy
from OSP.dota2_heatmap import render_heatmap
from OSP.steam_consumption import render_consumption_vis


@click.command()
@click.option('--func', default='consumption')
@click.option('--param', default=None)
def cli(func, param):
    if func == 'add league':
        add_league_matches(league_id=param, have_progress=True)
    elif func == 'calc match':
        print(calc_match_fantasy())
    elif func == 'heatmap':
        render_heatmap(param)
    elif func == 'consumption':
        render_consumption_vis()


if __name__ == '__main__':
    cli()
