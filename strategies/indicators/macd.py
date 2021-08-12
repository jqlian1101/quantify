from guess_indicators import guess_indicators
from common.get_hist_local import get_hist_data

# macd  DIF：12天平均和26天平均的差
# macds Signal macd9天均值
# macdh Histogram (柱): 计算macd与signal的差值
stock_column = ["macd", "macds", "macdh"]


def get_signal(df):
    stock_data = guess_indicators(df, stock_column)

    return stock_data


if '__main__' == __name__:
    df = get_hist_data('000001')

    stock = get_signal(df)

    print(stock)
    stock.to_csv('./output/macd.csv',
                 encoding="utf_8_sig")  # utf_8_sig 解决导出时中文乱码
