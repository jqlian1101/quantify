from matplotlib.pyplot import close
import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt
import mpl_finance as mpf
import pandas_datareader.data as web
import matplotlib.gridspec as gridspec # 分割子图

from utils import query_history


history_data = query_history.QueryHistory('sh.600000', ('2019-1-1', '2020-1-1'))
df = history_data.query_from_bs()


# 分别计算5日、20日、60日的移动平均线
ma_list = [5, 20, 60]
ma_line_color=['black','green','blue']

# 计算简单算术移动平均线MA – df.close 为股票每天的收盘价
for ma in ma_list:
    df['ma%d'%ma] = df.close.rolling(window=ma).mean()


# 创建fig对象
fig = plt.figure(figsize=(8,6), dpi=100, facecolor='white')

gs = gridspec.GridSpec(4, 1, left=0.08, bottom=0.10, right=0.94, top=0.96, wspace=0.2, hspace=0, height_ratios=[3.5, 1, 1, 1])
graph_KAV = fig.add_subplot(gs[0,:])        # k线
graph_VOL = fig.add_subplot(gs[1,:])        # 成交量
graph_MACD = fig.add_subplot(gs[2,:])       # macd
graph_KDJ = fig.add_subplot(gs[3,:])        # kdj

# # 调整边框距离
# fig.subplots_adjust(left=0.09, bottom=0.10, right=0.94,top=0.9, wspace=0.2, hspace=0)

data_len = len(df.index)

# 创建k线图
mpf.candlestick2_ochl(graph_KAV, df.open, df.close, df.high, df.low, width=0.5, colorup='r', colordown='g')

# 绘制均线
for index in range(len(ma_list)):
    cur_ma = ma_list[index]
    graph_KAV.plot(np.arange(0, data_len), df['ma%d'%cur_ma], ma_line_color[index], label='MA%d'%cur_ma, lw=1.0)

graph_KAV.legend(loc='best')
graph_KAV.set_title(u"600000 日K线")
graph_KAV.set_ylabel(u"价格")
graph_KAV.set_xlim(0, data_len)  # 设置一下x轴的范围


# 绘制成交量
graph_VOL.bar(np.arange(0, data_len), df.volume, color=['g' if df.open[x] > df.close[x] else 'r' for x in range(0, data_len) ])
graph_VOL.set_ylabel(u"成交量")
graph_VOL.set_xticks(range(0, data_len), 15)    # x轴范围，每15天标一个日期

# MACD
macd_dif, macd_dea, macd_bar = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)


# plt.show()
