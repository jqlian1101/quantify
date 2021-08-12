import os
import pandas as pd

# import tushare as ts

# ts.set_token('1fef20d253d2a005a6f6d89ee0c0c4627c48962a5ad89fed37cb4c68')
# tsPro = ts.pro_api()
# df = tsPro.daily(ts_code='600000.SH', start_date=start, end_date=end)


def get_hist_data(code):
    """读取本地历史数据
    从'files/history'中读取历史数据

    Args:
        code (str): stock code

    Returns:
    """
    pwd = os.path.realpath(__file__)
    work_dir = os.path.dirname(os.path.dirname(os.path.dirname(pwd)))
    history_dir = os.path.join(work_dir, 'files/history', code + '.csv')

    df = pd.read_csv(history_dir, encoding="utf-8", index_col=0)

    cols = {'ts_code': 'code', 'trade_date': 'date', 'vol': 'volume'}
    df.rename(columns=cols, inplace=True)

    df.insert(2, 'trade', df['close'])

    return df


if '__main__' == __name__:
    df = get_hist_data('000001')
    print(df)
