import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
import pandas_datareader.data as web
import datetime

from utils import query_history

# df_stockload = web.DataReader("600000.SS", "yahoo", datetime.datetime(2019,1,1), datetime.datetime(2020,1,1))

history_data = query_history.QueryHistory('sh.600000', ('2019-1-1', '2020-1-1'))
stock_data = history_data.query_from_bs()

# print(df_stockload.index)
# print(stock_data.index)

# 分别计算5日、20日、60日的移动平均线
ma_list = [5, 20, 60]

# # 计算简单算术移动平均线MA – stock_data.close 为股票每天的收盘价
# for ma in ma_list:
#     stock_data['ma%d'%ma] = stock_data.close.rolling(window=ma).mean()


# 创建fig对象
fig = plt.figure(figsize=(8,6), dpi=100, facecolor='white')
# 调整边框距离
fig.subplots_adjust(left=0.09, bottom=0.10, right=0.94,top=0.9, wspace=0.2, hspace=0)


# 创建k线图
graph_bar = fig.add_subplot(1,1,1)
mpf.candlestick2_ochl(graph_bar, stock_data.open, stock_data.close, stock_data.high, stock_data.low, width=0.5, colorup='r', colordown='g')

# 绘制K线图
# mpf.candlestick2_ochl(graph_bar, df_stockload.Open, df_stockload.Close, df_stockload.High, df_stockload.Low, width=0.5, colorup='r', colordown='g')  # 绘制K线走势

plt.show()
