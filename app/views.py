from flask import render_template
from .dota2_fantasy import calc_match_fantasy
from .dota2_heatmap import page as heatmap_page
from .steam_consumption import page as consumption_page
from . import app

REMOTE_HOST = 'https://pyecharts.github.io/assets/js'


@app.route('/fantasy/')
def fantasy():
    return render_template(
        'fantasy.html',
        fantasy_dict=calc_match_fantasy(3870838763),
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
def heatmap():
    _page = heatmap_page()
    return render_template(
        'pyecharts.html',
        myechart=_page.render_embed(),
        host=REMOTE_HOST,
        script_list=_page.get_js_dependencies(),
    )


@app.route('/')
def index():
    return 'hello world'
