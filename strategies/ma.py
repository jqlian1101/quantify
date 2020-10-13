
from utils import query_history

history_data = query_history.QueryHistory('sh.600000',('2019-1-1', '2020-1-1'))
df_stockload = history_data.query_from_bs()

#绘制移动平均线图
df_stockload['MA5'] = df_stockload.close.rolling(window=5).mean()
df_stockload['MA20'] = df_stockload.close.rolling(window=20).mean()
df_stockload['MA30'] = df_stockload.close.rolling(window=30).mean()


