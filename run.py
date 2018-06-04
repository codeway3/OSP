import sys
import click
sys.path.append('..')
from OSP.dota2_fantasy_prediction import add_league_matches, calc_match_fantasy
from OSP.dota2_heatmap import render_heatmap


@click.command()
@click.option('--func', default='add league')
@click.option('--param', default=9880)
def cli(func, param):
    if func == 'add league':
        add_league_matches(league_id=param, have_progress=True)
    elif func == 'calc match':
        print(calc_match_fantasy())
    elif func == 'heatmap':
        render_heatmap(1)


if __name__ == '__main__':
    cli()
