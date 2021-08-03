import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)  # 添加路径，这个是临时的

import stockstats
import pandas as pd
from common.get_hist_local import get_hist_data

stock_column = [
    'adx', 'adxr', 'boll', 'boll_lb', 'boll_ub', 'cci', 'cci_20', 'close_-1_r',
    'close_-2_r', 'cr', 'cr-ma1', 'cr-ma2', 'cr-ma3', 'dma', 'dx', 'kdjd',
    'kdjj', 'kdjk', 'macd', 'macdh', 'macds', 'mdi', 'pdi', 'rsi_12', 'rsi_6',
    'trix', 'trix_9_sma', 'vr', 'vr_6_sma', 'wr_10', 'wr_6'
]


def guess_indicators(df, column=stock_column):
    # 先按日期进行排序：2020-01-01 ～ 2020-12-30
    stock = df.sort_index(0)

    stockStat = stockstats.StockDataFrame.retype(stock)

    # 获取指标值
    stats = stockStat[column]

    # 将指标合并到原始数据
    data_new = pd.merge(df, stats, on=['date'], how='left')
    data_new = data_new.round(4)  # 数据保留4位小数

    return data_new


if __name__ == '__main__':
    df = get_hist_data('000001')
    stock = guess_indicators(df)

    print(stock)

    stock.to_csv('./output/indicators.csv', index=False,
                 encoding="utf_8_sig")  # utf_8_sig 解决导出时中文乱码
