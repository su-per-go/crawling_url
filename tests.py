from pyecharts import options as opts
from pyecharts.charts import Pie

# 数据
data = [
    {"name": '200', "value": 20592},
    {"name": '502', "value": 7271},
    {"name": '其他', "value": 205},
    {"name": '403', "value": 818},
    {"name": '522', "value": 77},
    {"name": '404', "value": 250},
    {"name": '0', "value": 133},
    {"name": '504', "value": 13},
    {"name": '429', "value": 8},
    {"name": '400', "value": 36},
    {"name": '523', "value": 14},
    {"name": '521', "value": 22},
    {"name": '421', "value": 5},
    {"name": '401', "value": 21},
    {"name": '405', "value": 10},
    {"name": '500', "value": 50},
    {"name": '412', "value": 1},
    {"name": '503', "value": 52},
    {"name": '525', "value": 5},
    {"name": '507', "value": 2},
    {"name": '524', "value": 1},
    {"name": '203', "value": 1},
    {"name": '410', "value": 12},
    {"name": '437', "value": 1},
    {"name": '688', "value": 1},
    {"name": '451', "value": 2},
    {"name": '417', "value": 1},
    {"name": '530', "value": 9},
    {"name": '550', "value": 1},
    {"name": '409', "value": 1},
    {"name": '419', "value": 1},
    {"name": '307', "value": 2},
    {"name": '555', "value": 1},
    {"name": '526', "value": 2},
    {"name": '202', "value": 1},
    {"name": '520', "value": 5},
    {"name": '719', "value": 1},
    {"name": '406', "value": 2},
    {"name": '432', "value": 1},
    {"name": '402', "value": 2},
]

# 创建饼图
pie_chart = (
    Pie(init_opts=opts.InitOpts(renderer='svg'))
    .add("", data, radius="65%", center=["50%", "50%"], rosetype="radius")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Weather Statistics", subtitle="Fake Data", pos_left="center"),
        # legend_opts=opts.LegendOpts(bottom=10, left="center"),
        tooltip_opts=opts.TooltipOpts(formatter="{a} <br/>{b} : {c} ({d}%)"),
    )
    # .set_series_opts(
    #     emphasis_opts=opts.EmphasisOpts(itemstyle_opts={"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"})
    # )
)

# 显示图表
pie_chart.render("weather_statistics.html")
