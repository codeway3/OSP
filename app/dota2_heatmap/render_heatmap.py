from datetime import datetime
from pyecharts import HeatMap, Page
from ..utils import get_player_matches_json


def page(player_id: int=None):
    # init_list = json_load('matches')
    if not player_id:
        init_list = get_player_matches_json(129689355)
    else:
        init_list = get_player_matches_json(player_id)
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

    page = Page()
    year = int(datetime.today().strftime("%Y"))
    for i in range(year, 2016, -1):
        heatmap = HeatMap(height=250, width=1100)
        heatmap.add("", data, is_calendar_heatmap=True,
                    visual_text_color='#000', visual_range_text=['', ''],
                    visual_range=[0, 15], calendar_cell_size=['auto', 20],
                    is_visualmap=True, calendar_date_range=str(i),
                    visual_orient="horizontal", visual_pos="center",
                    visual_top="90%", is_piecewise=True)
        page.add(heatmap)
    return page


def render_heatmap(player_id: int=None):
    _page = page(player_id)
    _page.render(path='./tmp/heatmap.html')
