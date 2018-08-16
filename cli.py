import click
from app.dota2_fantasy import calc_match_fantasy
from app.utils import add_league_matches, tmp_add_team_info
# from app.dota2_heatmap import render_heatmap
# from app.steam_consumption import render_consumption_vis


@click.command()
@click.option('--func', default='addleague', help='addleague/fantasy/teamsdeal')
@click.option('--param', default=None)
def cli(func, param):
    if func == 'addleague':
        add_league_matches(league_id=param, have_progress=True)
    elif func == 'fantasy':
        print(calc_match_fantasy(match_id=param))
    elif func == 'teamsdeal':
        tmp_add_team_info()
    # elif func == 'heatmap':
    #     render_heatmap(player_id=param)
    # elif func == 'consumption':
    #     render_consumption_vis()


if __name__ == '__main__':
    cli()
