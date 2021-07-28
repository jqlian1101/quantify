"""
海龟交易法则
"""

from typing import Any
import matplotlib.pyplot as plt
import datetime

from utils import query_history

history_data = query_history.QueryHistory(
    'sh.600000', ('2019-1-1', '2020-1-1'),
    cols=["date", "open", "high", "low", "close", "volume"])
df = history_data.query_from_bs()

N1 = 15
N2 = 5

# 从第N1天开始滚动计算该周期内最大值
df['n1_high'] = df.high.rolling(window=N1).max()
# 从收盘价序列第一个数据开始依次寻找当前为止的最大值来填充前N1个NaN
expan_max = df.close.expanding().max()
# 目前出现过的最大值填充前N1个nan
df['n1_high'].fillna(value=expan_max, inplace=True)

df['n2_low'] = df.low.rolling(window=N2).min()
expan_min = df.low.expanding().min()
df['n2_low'].fillna(value=expan_min, inplace=True)
# print(df)

# shift(1)的作用是在index不变的情况下对序列的值向右移动一个单位，
# 目的是获取昨天为止的最高价格，表示当日收盘价突破昨日为止最高价格时买入股票。
buy_index = df[df.close > df.n1_high.shift(1)].index
sell_index = df[df.close < df.n2_low.shift(1)].index

# 寻找到符合买入/卖出条件的时间序列后，以该时间序列构建signal序列，
# 将买入当天的signal值设置为1，代表买入，同理将signal设置为0，代表卖出。
df.loc[buy_index, 'signal'] = 1
df.loc[sell_index, 'signal'] = 0

df['signal'].fillna(method='ffill', inplace=True)

# 由于收盘价格是在收盘后才确定，那么第二天才能执行给出的买卖操作，此处将signal序列使用shift(1)方法右移更接近真实情况
df['signal'] = df['signal'].shift(1)

# -------------------------
# -------------------------
# 可视化

df.close.plot()

skip_days = 0
start = Any
end = Any

for kl_index, today in df.iterrows():
    if today.signal == 1 and skip_days == 0:  # 买入
        skip_days = -1
        start = df.index.get_loc(kl_index)
        plt.annotate('买入',
                     xy=(kl_index, df.close.asof(kl_index)),
                     xytext=(kl_index, df.close.asof(kl_index) + 2),
                     arrowprops=dict(facecolor='r', shrink=0.1),
                     horizontalalignment='left',
                     verticalalignment='top')

        print("buy: ", kl_index)

    elif today.signal == 0 and skip_days == -1:  # 卖出
        skip_days = 0
        end = df.index.get_loc(kl_index)

        if df.close[end] < df.close[start]:  # 赔钱显示绿色
            plt.fill_between(df.index[start:end],
                             0,
                             df.close[start:end],
                             color='green',
                             alpha=0.38)
        else:  # 赚钱显示红色
            plt.fill_between(df.index[start:end],
                             0,
                             df.close[start:end],
                             color='red',
                             alpha=0.38)

        plt.annotate('卖出',
                     xy=(kl_index, df.close.asof(kl_index)),
                     xytext=(kl_index + datetime.timedelta(days=5),
                             df.close.asof(kl_index) + 2),
                     arrowprops=dict(facecolor='g', shrink=0.1),
                     horizontalalignment='left',
                     verticalalignment='top')

        print("sell:", kl_index)

plt.legend(loc='best')
plt.title(u"sh.600000  N日突破择时")
plt.show()
