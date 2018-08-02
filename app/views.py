from flask import render_template
from .dota2_fantasy import calc_match_fantasy
from .dota2_heatmap import page as heatmap_page
from .steam_consumption import page as consumption_page
from . import app

REMOTE_HOST = 'https://pyecharts.github.io/assets/js'


@app.route('/fantasy/')
@app.route('/fantasy/<int:match_id>')
def fantasy(match_id=None):
    return render_template(
        'fantasy.html',
        fantasy_dict=calc_match_fantasy(match_id),
    )


@app.route('/consumption/')
def consumption():
    _page = consumption_page()
    return render_template(
        'pyecharts.html',
        myechart=_page.render_embed(),
        host=REMOTE_HOST,
        script_list=_page.get_js_dependencies(),
    )


@app.route('/heatmap/')
@app.route('/heatmap/<int:player_id>')
def heatmap(player_id=None):
    _page = heatmap_page(player_id)
    return render_template(
        'pyecharts.html',
        myechart=_page.render_embed(),
        host=REMOTE_HOST,
        script_list=_page.get_js_dependencies(),
    )


@app.route('/')
def index():
    return render_template(
        'index.html',
    )
