#-*-coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
import csv

# 日期，股票代码，名称，收盘价，最高价，最低价，开盘价，前收盘价，涨跌额，涨跌幅，换手率，成交量，成交额，总市值，流通市值
str = 'date,code,name,close,high,low,open,preclose,chg,pctChg,turn,volume,amount,tcap,mcap'
header_list = str.split(',')

pwd = os.path.split(os.path.realpath(__file__))[0]

# 转换前的文件存储路径
save_path = pwd + '/files/history/'

# 转换后文件的存储路径
cwdpath = os.path.abspath(os.path.dirname(pwd))
target_path = cwdpath + '/files/history/'


err_list = []
def handle_file(file_name):
    try:
        df = pd.read_csv(save_path + file_name, encoding = 'gbk', header=0)
        df.columns = header_list
        df.to_csv(target_path + file_name, index=False, encoding='utf-8')
    except:
        err_list.append(file_name)


# 获取已下载的股票列表
files = os.walk(save_path)

for i, j, k in files:
    for item in k:
        handle_file(item)


# # TODO 处理异常股票
# with open(cwdpath + '/err.csv', 'r+', newline='') as f:
#     reader = csv.reader(f)

#     for item in reader:
#         print(item)
#         print(item[0] + '.csv')
#         handle_file(item[0] + '.csv')


# 保存异常文件列表
err_path = cwdpath + '/err.csv'

# TODO pandas实现
# err_file = pd.DataFrame(columns=['code'], data=err_list, index=None)
# err_file.to_csv(cwdpath + 'err.csv', encoding='utf-8')


with open(cwdpath + '/err2.csv', 'w+', newline='') as f:
    writer = csv.writer(f)

    for i in range(len(err_list)):
        writer.writerow([err_list[i][:-4]])





