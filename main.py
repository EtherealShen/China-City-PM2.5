'''
@Description: 
@Author: Ambrose
@Date: 2024-05-20 16:48:13
@LastEditTime: 2024-05-20 21:31:11
@LastEditors: Ambrose
'''
import pandas as pd
import numpy as np
import os
import re
from pyecharts import options as opts
from pyecharts.charts import Line,Bar,Page,Scatter


class Weather_relation():
    def __init__(self):
        self.bj = pd.read_csv("./data/BeijingPM20100101_20151231.csv")
        self.cd = pd.read_csv("./data/ChengduPM20100101_20151231.csv")
        self.gz = pd.read_csv("./data/GuangzhouPM20100101_20151231.csv")
        self.sh = pd.read_csv("./data/ShanghaiPM20100101_20151231.csv")
        self.sy = pd.read_csv("./data/ShenyangPM20100101_20151231.csv")
    
    # 各个城市PM2.5平均值情况。
    def avg_PM(self):
        bj_mean = int((self.bj["PM_Dongsi"].mean() + self.bj["PM_Dongsihuan"].mean() + self.bj["PM_Nongzhanguan"].mean() + self.bj["PM_US Post"].mean())/4)
        cd_mean = int((self.cd["PM_Caotangsi"].mean() + self.cd["PM_Shahepu"].mean() + self.cd["PM_US Post"].mean())/3)
        gz_mean = int((self.gz["PM_City Station"].mean() + self.gz["PM_5th Middle School"].mean() + self.gz["PM_US Post"].mean())/3)
        sh_mean = int((self.sh["PM_Jingan"].mean() + self.sh["PM_US Post"].mean() + self.sh["PM_Xuhui"].mean())/3)
        sy_mean = int((self.sy["PM_Taiyuanjie"].mean() + self.sy["PM_US Post"].mean() + self.sy["PM_Xiaoheyan"].mean())/3)
        city_list = ["北京","成都","广州","上海","沈阳"]
        avg_PM = [bj_mean,cd_mean,gz_mean,sh_mean,sy_mean]

        bar_chart = (
            Bar()
            .set_global_opts(
                title_opts=opts.TitleOpts(title="城市平均 PM2.5 值图"),
                xaxis_opts=opts.AxisOpts(name="城市"),
                yaxis_opts=opts.AxisOpts(name="平均 PM 值"),
            )
            .add_xaxis(city_list)
            .add_yaxis("平均 PM 值", avg_PM)
        )

        bar_chart.render("./output/1-1.html")

    # 各个城市各年份PM2.5的平均值情况。
    def avg_year_PM(self):
        avg_year_bj = self.bj.groupby('year')[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']].mean()
        bj = avg_year_bj.fillna(0).mean(axis=1).round().astype(int).tolist()

        avg_year_cd = self.cd.groupby('year')[["PM_Caotangsi","PM_Shahepu","PM_US Post"]].mean()
        cd = avg_year_cd.fillna(0).mean(axis=1).round().astype(int).tolist()
        
        avg_year_gz = self.gz.groupby('year')[["PM_City Station","PM_5th Middle School","PM_US Post"]].mean()
        gz = avg_year_gz.fillna(0).mean(axis=1).round().astype(int).tolist()
        
        avg_year_sh = self.sh.groupby('year')[["PM_Jingan","PM_US Post","PM_Xuhui"]].mean()
        sh = avg_year_sh.fillna(0).mean(axis=1).round().astype(int).tolist()
        
        avg_year_sy = self.sy.groupby('year')[["PM_Taiyuanjie","PM_US Post","PM_Xiaoheyan"]].mean()
        sy = avg_year_sy.fillna(0).mean(axis=1).round().astype(int).tolist()
        
        bar_chart = (
            Bar()
            .add_xaxis(['2010', '2011', '2012', '2013', '2014', '2015'])
            .add_yaxis("北京", bj)
            .add_yaxis("成都", cd)
            .add_yaxis("广州", gz)
            .add_yaxis("上海", sh)
            .add_yaxis("沈阳", sy)
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
                title_opts=opts.TitleOpts(title="PM2.5 Average by Year"),
                yaxis_opts=opts.AxisOpts(name="Average PM2.5"),
            )
        )
        bar_chart.render("./output/1-2.html")
 
    # 各个城市PM2.5随季节的变化情况。
    def relation_PM_season(self):
        path = "./data"
        files_name = os.listdir(path)

        line = (
            Line()
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(name="季度"),
                yaxis_opts=opts.AxisOpts(name="PM2.5浓度(ug / m ^ 3)"),
                title_opts=opts.TitleOpts(title="5个城市PM2.5随季节的变化情况"),
            )
        )

        for file in files_name:
            position = path + "/" + file
            PM_datas = []
            for x in pd.read_csv(position, sep=',', header='infer', usecols=[2, 6, 7, 8]).values:
                if not (np.isnan(x[1]) and np.isnan(x[2]) and np.isnan(x[3])):
                    if not (np.isnan(x[1]) or np.isnan(x[2]) or np.isnan(x[3])):
                        average = (x[1] + x[2] + x[3]) / 3
                    elif not ((np.isnan(x[0]) or np.isnan(x[1])) and (np.isnan(x[1]) or np.isnan(x[2])) and (np.isnan(x[0]) or np.isnan(x[2]))):
                        if np.isnan(x[1]):
                            x[1] = 0
                        if np.isnan(x[2]):
                            x[2] = 0
                        if np.isnan(x[3]):
                            x[3] = 0
                        average = (x[1] + x[2] + x[3]) / 2
                    else:
                        if not np.isnan(x[1]):
                            average = x[1]
                        if not np.isnan(x[2]):
                            average = x[2]
                        if not np.isnan(x[3]):
                            average = x[3]
                    PM_datas.append((int(x[0]), average))
            
            season_data_dict = {1: 0, 2: 0, 3: 0, 4: 0}
            season_sum_dict = {1: 0, 2: 0, 3: 0, 4: 0}
            
            for PM_data in PM_datas:
                if 1 <= PM_data[0] <= 3:
                    season_data_dict[1] += 1
                    season_sum_dict[1] += PM_data[1]
                elif 4 <= PM_data[0] <= 6:
                    season_data_dict[2] += 1
                    season_sum_dict[2] += PM_data[1]
                elif 7 <= PM_data[0] <= 9:
                    season_data_dict[3] += 1
                    season_sum_dict[3] += PM_data[1]
                else:
                    season_data_dict[4] += 1
                    season_sum_dict[4] += PM_data[1]

            season_data_ls = [(x, round(season_sum_dict[x] / season_data_dict[x], 2)) for x in season_data_dict]
            name_ls = [str(x[0]) for x in season_data_ls]
            data_ls = [x[1] for x in season_data_ls]
            
            line.add_xaxis(name_ls).add_yaxis(
                re.sub("[P][M].*", "", file),
                data_ls,
                symbol="triangle",
            )

        line.set_series_opts(label_opts=opts.LabelOpts(position="top", formatter="{c}"))
        line.render("./output/1-3.html")

    # 各个城市PM2.5随月份的变化情况。
    def relation_PM_month(self):
        path = "./data"
        files_name = os.listdir(path)
        line = Line()
        for i, file in enumerate(files_name):
            position = path + "/" + file
            PM_datas = []
            for x in pd.read_csv(position, sep=',', header='infer', usecols=[2, 6, 7, 8]).values:
                if not (np.isnan(x[1]) and np.isnan(x[2]) and np.isnan(x[3])):
                    if not (np.isnan(x[1]) or np.isnan(x[2]) or np.isnan(x[3])):
                        average = (x[1] + x[2] + x[3]) / 3
                    elif not ((np.isnan(x[0]) or np.isnan(x[1])) and (np.isnan(x[1]) or np.isnan(x[2])) and (np.isnan(x[0]) or np.isnan(x[2]))):
                        if np.isnan(x[1]):
                            x[1] = 0
                        if np.isnan(x[2]):
                            x[2] = 0
                        if np.isnan(x[3]):
                            x[3] = 0
                        average = (x[1] + x[2] + x[3]) / 2
                    else:
                        if not np.isnan(x[1]):
                            average = x[1]
                        if not np.isnan(x[2]):
                            average = x[2]
                        if not np.isnan(x[3]):
                            average = x[3]
                    PM_datas.append((int(x[0]), average))
            month_data_dict = {}
            month_sum_dict = {}
            for PM_data in PM_datas:
                if PM_data[0] in month_data_dict and PM_data[0] in month_sum_dict:
                    month_data_dict[PM_data[0]] += 1
                    month_sum_dict[PM_data[0]] += PM_data[1]
                else:
                    month_data_dict[PM_data[0]] = 1
                    month_sum_dict[PM_data[0]] = PM_data[1]
            
            month_data_ls = [(x, round(month_sum_dict[x] / month_data_dict[x], 2)) for x in month_data_dict]
            month_data_ls.sort(key=lambda x: x[0])
            name_ls = [str(x[0]) for x in month_data_ls]
            data_ls = [x[1] for x in month_data_ls]
            
            line.add_xaxis(name_ls)
            line.add_yaxis(re.sub("[P][M].*", "", file), data_ls, symbol="triangle", linestyle_opts=opts.LineStyleOpts(width=3), label_opts=opts.LabelOpts(is_show=False))
            line.set_series_opts(label_opts=opts.LabelOpts(position="top", formatter="{c}", is_show=False))
        
        line.set_global_opts(xaxis_opts=opts.AxisOpts(name="月份"), yaxis_opts=opts.AxisOpts(name="PM2.5浓度(ug / m ^ 3)"), title_opts=opts.TitleOpts(title="中国5个城市PM2.5浓度随月份变化情况",pos_bottom=0))
        line.render("./output/1-4.html")      

    # 各个城市PM2.5随日的变化情况
    def relation_PM_date(self):
        path = "./data"
        files_name = os.listdir(path)
        line = Line()
        for file in files_name:
            position = path + "/" + file
            PM_datas = []
            for x in pd.read_csv(position, sep=',', header='infer', usecols=[3, 6, 7, 8]).values:
                if not (np.isnan(x[1]) and np.isnan(x[2]) and np.isnan(x[3])):
                    if not (np.isnan(x[1]) or np.isnan(x[2]) or np.isnan(x[3])):
                        average = (x[1] + x[2] + x[3]) / 3
                    elif not ((np.isnan(x[0]) or np.isnan(x[1])) and (np.isnan(x[1]) or np.isnan(x[2])) and (np.isnan(x[0]) or np.isnan(x[2]))):
                        if np.isnan(x[1]):
                            x[1] = 0
                        if np.isnan(x[2]):
                            x[2] = 0
                        if np.isnan(x[3]):
                            x[3] = 0
                        average = (x[1] + x[2] + x[3]) / 2
                    else:
                        if not np.isnan(x[1]):
                            average = x[1]
                        if not np.isnan(x[2]):
                            average = x[2]
                        if not np.isnan(x[3]):
                            average = x[3]
                    PM_datas.append((int(x[0]), average))
            day_data_dict = {}
            day_sum_dict = {}
            for PM_data in PM_datas:
                if PM_data[0] in day_data_dict and PM_data[0] in day_sum_dict:
                    day_data_dict[PM_data[0]] += 1
                    day_sum_dict[PM_data[0]] += PM_data[1]
                else:
                    day_data_dict[PM_data[0]] = 1
                    day_sum_dict[PM_data[0]] = PM_data[1]
            day_data_ls = [(x, round(day_sum_dict[x] / day_data_dict[x], 2)) for x in day_data_dict]
            day_data_ls.sort(key=lambda x: x[0])
            name_ls = [str(x[0]) for x in day_data_ls]
            data_ls = [x[1] for x in day_data_ls]
            
            line.add_xaxis(name_ls)
            line.add_yaxis(re.sub("[P][M].*", "", file), data_ls, symbol="triangle", linestyle_opts=opts.LineStyleOpts(width=3), label_opts=opts.LabelOpts(is_show=False))
            line.set_series_opts(label_opts=opts.LabelOpts(position="top", formatter="{c}", is_show=False))


        line.set_global_opts(xaxis_opts=opts.AxisOpts(name="月份"), yaxis_opts=opts.AxisOpts(name="PM2.5浓度(ug / m ^ 3)"), title_opts=opts.TitleOpts(title="中国5个城市PM2.5浓度随日变化情况",pos_bottom=0))
        line.render("./output/1-5.html") 

    # 各个城市各年份降水量的平均值情况。
    def avg_year_rain(self):
        path = "./data"
        files_name = os.listdir(path)

        page = Page()
        for file in files_name:
            position = path + "/" + file
            PM_datas = []
            for x in pd.read_csv(position, sep=',', header='infer', usecols=[1, 16]).values:
                if not np.isnan(x[1]):
                    PM_datas.append((int(x[0]), x[1]))
            year_data_dict = {}
            year_sum_dict = {}
            for PM_data in PM_datas:
                if PM_data[0] in year_data_dict and PM_data[0] in year_sum_dict:
                    year_data_dict[PM_data[0]] += 1
                    year_sum_dict[PM_data[0]] += PM_data[1]
                else:
                    year_data_dict[PM_data[0]] = 1
                    year_sum_dict[PM_data[0]] = PM_data[1]
            
            year_data_ls = [(x, round(year_sum_dict[x] / year_data_dict[x], 2)) for x in year_data_dict]
            name_list = [x[0] for x in year_data_ls]
            data_ls = [x[1] for x in year_data_ls]
            
            bar = (
                Bar()
                .add_xaxis(name_list)
                .add_yaxis("", data_ls, label_opts=opts.LabelOpts(position="top", formatter="{c}"))
                .set_global_opts(
                    xaxis_opts=opts.AxisOpts(name="年份"),
                    yaxis_opts=opts.AxisOpts(name="降水量(毫米)"),
                    title_opts=opts.TitleOpts(title=re.sub("[P][M].", "", file) + "各年份降水量平均值情况"),
                )
            )
            
            page.add(bar)
        page.render("./output/2-1.html")                

    # 各个城市降水量随季节的变化情况
    def relation_rain_season(self):
        path = "./data"
        files_name = os.listdir(path)

        page = Page()
        for file in files_name:
            position = path + "/" + file
            PM_datas = []
            for x in pd.read_csv(position, sep=',', header='infer', usecols=[2, 16]).values:
                if not np.isnan(x[1]):
                    PM_datas.append((int(x[0]), x[1]))
            season_data_dict = {1: 0, 2: 0, 3: 0, 4: 0}
            season_sum_dict = {1: 0, 2: 0, 3: 0, 4: 0}
            for PM_data in PM_datas:
                if 1 <= PM_data[0] <= 3:
                    season_data_dict[1] += 1
                    season_sum_dict[1] += PM_data[1]
                elif 4 <= PM_data[0] <= 6:
                    season_data_dict[2] += 1
                    season_sum_dict[2] += PM_data[1]
                elif 7 <= PM_data[0] <= 9:
                    season_data_dict[3] += 1
                    season_sum_dict[3] += PM_data[1]
                else:
                    season_data_dict[4] += 1
                    season_sum_dict[4] += PM_data[1]
            season_data_ls = [(x, round(season_sum_dict[x] / season_data_dict[x], 2)) for x in season_data_dict]
            name_ls = [str(x[0]) for x in season_data_ls]
            data_ls = [x[1] for x in season_data_ls]
            
            line = (
                Line()
                .add_xaxis(name_ls)
                .add_yaxis(
                    "",
                    data_ls,
                    symbol="emptyCircle",
                    symbol_size=8,
                    linestyle_opts=opts.LineStyleOpts(color="gray", width=1, type_="dashed"),
                    label_opts=opts.LabelOpts(position="top", formatter="{c}"),
                )
                .set_global_opts(
                    xaxis_opts=opts.AxisOpts(name="季度"),
                    yaxis_opts=opts.AxisOpts(name="降水量(毫米)"),
                    title_opts=opts.TitleOpts(title=re.sub("[P][M].*", "", file) + "降水量随季节的变化情况"),
                )
            )
            
            page.add(line)
        page.render("./output/2-2.html")

    # 各个城市降水量随月份的变化情况。
    def relation_rain_month(self):
        path = "./data"
        files_name = os.listdir(path)

        page = Page()
        for file in files_name:
            position = path + "/" + file
            PM_datas = []
            for x in pd.read_csv(position, sep=',', header='infer', usecols=[2, 16]).values:
                if not np.isnan(x[1]):
                    PM_datas.append((int(x[0]), x[1]))
            month_data_dict = {}
            month_sum_dict = {}
            for PM_data in PM_datas:
                if PM_data[0] in month_data_dict and PM_data[0] in month_sum_dict:
                    month_data_dict[PM_data[0]] += 1
                    month_sum_dict[PM_data[0]] += PM_data[1]
                else:
                    month_data_dict[PM_data[0]] = 1
                    month_sum_dict[PM_data[0]] = PM_data[1]
            month_data_ls = [(x, round(month_sum_dict[x] / month_data_dict[x], 2)) for x in month_data_dict]
            name_ls = [str(x[0]) for x in month_data_ls]
            data_ls = [x[1] for x in month_data_ls]
            
            line = (
                Line()
                .add_xaxis(name_ls)
                .add_yaxis(
                    "",
                    data_ls,
                    symbol="emptyCircle",
                    symbol_size=8,
                    linestyle_opts=opts.LineStyleOpts(color="gray", width=1, type_="dashed"),
                    label_opts=opts.LabelOpts(position="top", formatter="{c}"),
                )
                .set_global_opts(
                    xaxis_opts=opts.AxisOpts(name="月份"),
                    yaxis_opts=opts.AxisOpts(name="降水量(毫米)"),
                    title_opts=opts.TitleOpts(title=re.sub("[P][M].*", "", file) + "降水量随月份的变化情况"),
                )
            )
            
            page.add(line)

        page.render("./output/2-3.html")

    # PM2.5与各城市风速关系。
    def relation_PM_wind(self):
        path = "./data"
        files_name = os.listdir(path)

        for file in files_name:
            position = path + "/" + file
            union_datas = []
            for x in pd.read_csv(position, sep=',', header='infer', usecols=[6, 7, 8, 14]).values:
                if not pd.isnull(x[3]):
                    if not (pd.isnull(x[0]) and pd.isnull(x[1]) and pd.isnull(x[2])):
                        if not (pd.isnull(x[0]) or pd.isnull(x[1]) or pd.isnull(x[2])):
                            average = (x[0] + x[1] + x[2]) / 2
                        elif not ((pd.isnull(x[0]) or pd.isnull(x[0])) and (pd.isnull(x[0]) or pd.isnull(x[1])) and (pd.isnull(x[0]) or pd.isnull(x[1]))):
                            if pd.isnull(x[0]):
                                x[0] = 0
                            if pd.isnull(x[1]):
                                x[1] = 0
                            if pd.isnull(x[2]):
                                x[2] = 0
                            average = (x[0] + x[1] + x[2]) / 1
                        else:
                            if not pd.isnull(x[0]):
                                average = x[0]
                            if not pd.isnull(x[1]):
                                average = x[1]
                            if not pd.isnull(x[2]):
                                average = x[2]
                        union_datas.append((x[3], average))
            iws_data_dict = {}
            iws_sum_dict = {}
            for union_data in union_datas:
                if union_data[0] in iws_data_dict and union_data[0] in iws_sum_dict:
                    iws_data_dict[union_data[0]] += 1
                    iws_sum_dict[union_data[0]] += union_data[1]
                else:
                    iws_data_dict[union_data[0]] = 1
                    iws_sum_dict[union_data[0]] = union_data[1]
            iws_data_ls = [(x, round(iws_sum_dict[x] / iws_data_dict[x], 2)) for x in iws_data_dict]
            iws_data_ls.sort(key=lambda x: x[0])
            
            line = (
                Line()
                .add_xaxis([x[0] for x in iws_data_ls])
                .add_yaxis(
                    "风速对应平均PM2.5浓度",
                    [x[1] for x in iws_data_ls],
                    symbol_size=8,
                    linestyle_opts=opts.LineStyleOpts(width=2),
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="PM2.5与" + re.sub("[P][M].*", "", file) + "城市风速关系(散点拟合图)"
                    ),
                    xaxis_opts=opts.AxisOpts(name="风速(m/s)"),
                    yaxis_opts=opts.AxisOpts(name="平均PM2.5浓度(ug / m ^ 3)"),
                    legend_opts=opts.LegendOpts(pos_right="top"),
                )
            )
            line.render("./output/3-" + re.sub("[P][M].*", "", file) + ".html")
                
 
if __name__ == "__main__":
    wr = Weather_relation()
    wr.avg_year_PM()
    wr.avg_PM()
    wr.relation_PM_season()
    wr.relation_PM_month()
    wr.relation_PM_date()
    wr.avg_year_rain()
    wr.relation_rain_season()
    wr.relation_rain_month()
    wr.relation_PM_wind()
