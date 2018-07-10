import click
from app.dota2_fantasy import add_league_matches, calc_match_fantasy
from app.dota2_heatmap import render_heatmap
from app.steam_consumption import render_consumption_vis


@click.command()
@click.option('--func', default='heatmap', help='add league/fantasy/heatmap/consumption')
@click.option('--param', default=None)
def cli(func, param):
    if func == 'add league':
        add_league_matches(league_id=param, have_progress=True)
    elif func == 'fantasy':
        print(calc_match_fantasy(match_id=param))
    elif func == 'heatmap':
        render_heatmap(player_id=param)
    elif func == 'consumption':
        render_consumption_vis()


if __name__ == '__main__':
    cli()
