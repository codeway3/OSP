import sys
from flask import Flask, render_template
sys.path.append('..')
from OSP.dota2_fantasy import calc_match_fantasy
from OSP.dota2_heatmap import page as heatmap_page
from OSP.steam_consumption import page as consumption_page

REMOTE_HOST = 'https://pyecharts.github.io/assets/js'


app = Flask(__name__)
app.config.from_object('config')


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
