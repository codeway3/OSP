from datetime import datetime
from pyecharts import HeatMap, Page
from ..utils import fetch_player_matches_json


def page(player_id: int=None):
    # init_list = json_load('matches')
    if not player_id:
        init_list = fetch_player_matches_json(129689355)
    else:
        init_list = fetch_player_matches_json(player_id)
    # print(len(init_list))
    init_dict = {}
    data = []
    for row in init_list:
        start_time = datetime.fromtimestamp(row['start_time']).strftime("%Y-%m-%d")
        if start_time not in init_dict:
            init_dict[start_time] = 1
        else:
            init_dict[start_time] += 1
    for key in init_dict:
        val = init_dict[key]
        key = datetime.strptime(key, "%Y-%m-%d")
        tmp = []
        tmp.extend((key, val))
        data.append(tmp)
    heatmap1 = HeatMap("日历热力图", "2017-2018年每日dota2游戏场数", height=250, width=1100)
    heatmap1.add("", data, is_calendar_heatmap=True,
                 visual_text_color='#000', visual_range_text=['', ''],
                 visual_range=[0, 15], calendar_cell_size=['auto', 20],
                 is_visualmap=True, calendar_date_range='2017',
                 visual_orient="horizontal", visual_pos="center",
                 visual_top="90%", is_piecewise=True)
    heatmap2 = HeatMap(height=250, width=1100)
    heatmap2.add("", data, is_calendar_heatmap=True,
                 visual_text_color='#000', visual_range_text=['', ''],
                 visual_range=[0, 15], calendar_cell_size=['auto', 20],
                 is_visualmap=True, calendar_date_range='2018',
                 visual_orient="horizontal", visual_pos="center",
                 visual_top="90%", is_piecewise=True)
    page = Page()
    page.add(heatmap1)
    page.add(heatmap2)
    return page


def render_heatmap(player_id: int=None):
    _page = page(player_id)
    _page.render(path='./tmp/heatmap.html')
