from guess_indicators import guess_indicators
from common.get_hist_local import get_hist_data

from common.backtrack import backtrack

# DIF
#   MACD Line (macd) ：12天平均和26天平均的差, (12-day EMA - 26-day EMA)
#
# DEA
#   Signal Line (macds): macd 9天均值, 9-day EMA of MACD Line
#
# MACD Histogram (macdh): 计算macd与signal的差值, MACD Line - Signal Line
stock_column = ["macd", "macds", "macdh"]


def get_signal(df):
    stock_data = guess_indicators(df, stock_column)
    stock_data['signal'] = 0

    stock_data['dif'] = stock_data['macd']
    stock_data['dea'] = stock_data['macds']

    stock_data['prev_dif'] = stock_data['macd'].shift(1)
    stock_data['prev_dif'].fillna(value=0, inplace=True)

    stock_data['prev_dea'] = stock_data['macds'].shift(1)
    stock_data['prev_dea'].fillna(value=0, inplace=True)

    # 金叉
    golden_crossing = (stock_data.prev_dif <
                       stock_data.prev_dea) & (stock_data.dif > stock_data.dea)
    golden_crossing_index = stock_data[golden_crossing].index

    # 死叉
    dead_crossing = (stock_data.prev_dif >
                     stock_data.prev_dea) & (stock_data.dif < stock_data.dea)
    dead_crossing_index = stock_data[dead_crossing].index

    stock_data.loc[golden_crossing_index, 'signal'] = 1
    stock_data.loc[dead_crossing_index, 'signal'] = -1

    return stock_data.drop(columns=['dif', 'dea', 'prev_dif', 'prev_dea'])


if '__main__' == __name__:
    df = get_hist_data('000001')
    df = df.sort_index(axis=0)
    df = df['1991-04-03':]
    # print(df)

    stock = get_signal(df)

    print(stock)

    output_stock = stock[["macd", "macds", "macdh", "signal"]]

    output_stock.to_csv('./output/macd.csv',
                        encoding="utf_8_sig")  # utf_8_sig 解决导出时中文乱码

    backtrack(stock)
