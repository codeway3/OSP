from pyecharts import Bar, Line, Page
from .data_processing import key_lst, val_lst, sum_lst


def render_consumption_vis():
    line = Line('Steam总计消费折线图')
    line.add('总计消费', key_lst, sum_lst, xaxis_rotate=45, yaxis_formatter="元", is_datazoom_show=True, datazoom_range=[0, 100], datazoom_type='inside', is_random=True)
    bar = Bar('Steam单笔消费柱状图')
    bar.add('单笔消费', key_lst, val_lst, mark_line=['average'], mark_point=['max', 'min'], xaxis_rotate=45, yaxis_formatter="元", is_datazoom_show=True, datazoom_range=[0, 100], datazoom_type='inside', is_random=True)

    page = Page()
    page.add(line)
    page.add(bar)
    page.render(path='./tmp/consumption.html')
