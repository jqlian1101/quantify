from guess_indicators import guess_indicators
from common.get_hist_local import get_hist_data
from common.backtrack import backtrack

stock_column = ['kdjd', 'kdjj', 'kdjk']

# 超买线
over_buy_signal = 80

# 超卖线
over_sell_signal = 20


def _get_kdj(df):
    return guess_indicators(df, stock_column)


def get_signal(df):
    """
    金叉 & 死叉获取买卖点
    """

    stock_data = _get_kdj(df)

    kdj_position = stock_data['kdjk'] > stock_data['kdjd']

    # golden crossing
    golden_index = kdj_position[(kdj_position == True)
                                & (kdj_position.shift() == False)].index

    # dead crossing
    dead_index = kdj_position[(kdj_position == False)
                              & (kdj_position.shift() == True)].index

    stock_data.loc[golden_index, 'signal'] = 1
    stock_data.loc[dead_index, 'signal'] = -1

    # 超买区出现死叉
    over_buy_golden = stock_data[(stock_data['kdjk'] > 80)
                                 & (stock_data['signal'] == -1)].index

    # 超卖区出现金叉
    over_sell_dead = stock_data[(stock_data['kdjk'] < 20)
                                & (stock_data['signal'] == 1)].index

    stock_data.loc[over_buy_golden, 'signal_2'] = -1
    stock_data.loc[over_sell_dead, 'signal_2'] = 1

    # # 由于收盘价格是在收盘后才确定，那么第二天才能执行给出的买卖操作，此处将signal序列使用shift(1)方法右移更接近真实情况，
    # stock_data['signal'] = stock_data.signal.shift(1)
    # stock_data['signal_2'] = stock_data.signal.shift(1)

    # stock_data['signal'].fillna(method='ffill', inplace=True)  # 与前面元素值保持一致
    stock_data['signal'].fillna(value=0, inplace=True)  # 默认用 0 填充
    stock_data['signal_2'].fillna(value=0, inplace=True)  # 默认用 0 填充

    return stock_data


if '__main__' == __name__:
    df = get_hist_data('000001')
    df = df.sort_index(axis=0)

    stock = get_signal(df)

    # print('=' * 100)
    # print(stock)

    output_stock = stock[[
        'close', 'kdjk', 'kdjd', 'kdjj', 'signal', 'signal_2'
    ]]

    # 输出到文件
    output_stock.to_csv('./output/kdj.csv',
                        encoding="utf_8_sig")  # utf_8_sig 解决导出时中文乱码

    backtrack(stock)
