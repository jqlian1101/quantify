'''
# -*- coding:UTF-8 -*-

# ATR（Average True Range）平均真实波动范围

# 真实波幅TR
# TR = MAX[(当日最高价-当日最低价)、abs(当日最高价-昨日收盘价)、abs(昨日收盘价-当日最低价)]
# TR = max(high-low, abs(last-high), abs(last-low))

# 真实波幅TR进行N日移动平均计算
# ATR = MA(TR, N)   参数N: 14日或21日
'''

import talib

from common import query_history

# history_data = query_history.QueryHistory('sh.600000', ('2019-1-1', '2020-1-1'))
# stockdata = history_data.query_from_bs()

# # 收盘价
# close = np.array(stockdata['close'])
# # 最高价
# high = np.array(stockdata['high'])
# # 最低价
# low = np.array(stockdata['low'])

# atr = talib.ATR(high, low, close, timeperiod = 14)


def GetStockDataApi(stockName=None,
                    startTime=None,
                    endTime=None,
                    N1=15,
                    N2=5,
                    n_loss=0.8,
                    n_win=2):
    """
    ATR值作为止盈止损的基准值，
    止盈值设置为 n_win 倍 的 ATR 值，
    止损值设置为 n_loss 倍 的 ATR 值，

    n_win 和 n_loss 分别为最大止盈系数和最大止损系数，
    此处设置最大止盈系数为2，最大止损系数为0.8，倾向于盈利值要大于亏损值。触发止盈止损条件为：

        n_win * ATR  > (今日收盘价格 - 买入价格)，触发止盈信号，卖出股票
        n_loss * ATR > (买入价格 - 今日收盘价格)，触发止损信号，卖出股票

    """

    history_data = query_history.QueryHistory('sh.%s' % stockName,
                                              (startTime, endTime))
    stockdata = history_data.query_from_bs()

    # 计算最近N1个交易日的最高价
    stockdata['N1_high'] = stockdata.high.rolling(window=N1).max()
    stockdata['N1_high'] = stockdata.N1_high.shift(1)
    expan_max = stockdata.close.expanding().max()
    stockdata['N1_high'].fillna(value=expan_max,
                                inplace=True)  # 目前出现过的最大值填充前N1个nan

    # 计算最近N2个交易日最低价
    stockdata['N2_low'] = stockdata.low.rolling(window=N2).min()
    stockdata['N2_low'] = stockdata.N2_low.shift(1)
    expan_min = stockdata.close.expanding().min()
    stockdata['N2_low'].fillna(value=expan_min,
                               inplace=True)  # 目前出现过的最小值填充前N2个nan

    stockdata['atr14'] = talib.ATR(stockdata.high.values,
                                   stockdata.low.values,
                                   stockdata.close.values,
                                   timeperiod=14)

    buy_price = 0

    for kl_index, today in stockdata.iterrows():
        # 收盘价超过N1最高价 买入股票持有
        if today.close > today.N1_high:
            print('N_day_buy : ', kl_index, today.close)
            buy_price = today.close
            stockdata.loc[kl_index, 'signal'] = 1

        # 到达收盘价少于买入价后触发卖出
        elif (buy_price != 0) and (buy_price > today.close) and (
            (buy_price - today.close) > n_loss * today.atr14):
            print('stop_loss_n : ', kl_index, today.close, buy_price)
            stockdata.loc[kl_index, 'signal'] = 0
            buy_price = 0

        # 到达收盘价多于买入价后触发卖出
        elif (buy_price != 0) and (buy_price < today.close) and (
            (today.close - buy_price) > n_win * today.atr14):
            print('stop_win_n : ', kl_index, today.close, buy_price)
            stockdata.loc[kl_index, 'signal'] = 0

        # 收盘价超过N2最低价 卖出股票持有
        elif today.close < today.N2_low:
            print('N_day_sell : ', kl_index, today.close, buy_price)
            stockdata.loc[kl_index, 'signal'] = 0
            buy_price = 0

        else:
            pass

    stockdata['signal'].fillna(method='ffill', inplace=True)
    stockdata['signal'] = stockdata.signal.shift(1)
    stockdata['signal'].fillna(method='bfill', inplace=True)

    return stockdata


if '__main__' == __name__:

    df = GetStockDataApi('600000', '2019-01-01', '2020-01-01')
