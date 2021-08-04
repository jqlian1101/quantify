from guess_indicators import guess_indicators
from common.get_hist_local import get_hist_data

stock_column = ['kdjd', 'kdjj', 'kdjk']


def get_signal_by_golden_dead_cross(df):
    """金叉 & 死叉获取买卖点"""
    stock_data = guess_indicators(df, stock_column)

    kdj_position = stock_data['kdjk'] > stock_data['kdjd']

    # golden crossing
    golden_index = kdj_position[(kdj_position == True)
                                & (kdj_position.shift() == False)].index

    # dead crossing
    dead_index = kdj_position[(kdj_position == False)
                              & (kdj_position.shift() == True)].index

    stock_data.loc[golden_index, 'signal'] = 1
    stock_data.loc[dead_index, 'signal'] = -1

    # 由于收盘价格是在收盘后才确定，那么第二天才能执行给出的买卖操作，此处将signal序列使用shift(1)方法右移更接近真实情况，
    stock_data['signal'] = stock_data.signal.shift(1)

    stock_data['signal'].fillna(method='ffill', inplace=True)  # 与前面元素值保持一致
    stock_data['signal'].fillna(value=-1, inplace=True)  # 序列最前面几个NaN值用-1填充

    return stock_data


if '__main__' == __name__:
    df = get_hist_data('000001')

    stock = get_signal_by_golden_dead_cross(df)

    print(stock)
    stock.to_csv('./output/kdj.csv',
                 encoding="utf_8_sig")  # utf_8_sig 解决导出时中文乱码
