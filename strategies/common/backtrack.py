import math

default_cash = 10000


def backtrack(df, signal_key="signal", buy_key="close"):
    cash = default_cash
    position = 0

    # df = df.sort_index(axis=0)

    df = df['2019-01-01':'2019-12-30']

    for index, row in df.iterrows():
        if row[signal_key] == 1 and position == 0 and row[buy_key] != 0:  # 买入股票
            position = math.floor((cash / row[buy_key]) / 100)
            position = position * 100

            buy_cash = position * row[buy_key]
            cash = cash - buy_cash

            print('{}买入{}股，买入价格{}元'.format(index, position, row[buy_key]))

        elif row[signal_key] == -1 and position != 0:  # 卖出持仓
            print('{}卖出{}，卖出价格{}'.format(index, position, row[buy_key]))

            sell_cash = position * row[buy_key]
            cash = cash + sell_cash
            position = 0

    assets = cash + position * df.iloc[0][buy_key]
    profit = round(assets - default_cash, 2)

    print('总资产：{}，现金：{}，持仓：{}'.format(round(assets, 2), round(cash, 2),
                                      round(position, 2)))
    print('盈利：{}'.format(profit))
