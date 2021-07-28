import talib
# from utils import query_history
import tushare as ts

# history_data = query_history.QueryHistory('sh.600000')

# df = history_data.query_from_local()

ts.set_token('1fef20d253d2a005a6f6d89ee0c0c4627c48962a5ad89fed37cb4c68')
tsPro = ts.pro_api()

df = tsPro.daily(ts_code='600000.SH',
                 start_date='20000101',
                 end_date='20210720')

# print(df.head(10))

####################
# 两字乌鸦
'''
以3日K线为参考，第一日长阳，第二日高开收阴，第三日再次高开收阴，同时收盘比前一日收盘价低，出现该形态预示着股价将要下跌
'''
# df['2_crows'] = talib.CDL2CROWS(df['open'].values, df['high'].values,
#                                 df['low'].values, df['close'].values)

# pattern = df[(df['2_crows'] == 100) | (df['2_crows'] == -100)]

####################
# 三只乌鸦
'''
看三日的K线，也就是连续三根阴线，而且每日收盘价都下跌且接近最低价，同时每日开盘价都在上根K线实体内，同样预示股价下跌。
'''
# df['three_crows'] = talib.CDL3BLACKCROWS(df['open'].values, df['high'].values,
#                                          df['low'].values, df['close'].values)
# pattern = df[(df['three_crows'] == 100) | (df['three_crows'] == -100)]

####################
# 十字星
'''
一日K线模式，定义为开盘价与收盘价基本相等，同时上下影线不会很长，预示着当前趋势反转。
'''
# df['star'] = talib.CDLDOJISTAR(df['open'].values, df['high'].values,
#                                df['low'].values, df['close'].values)

# pattern = df[(df['star'] == 100) | (df['star'] == -100)]

####################
# 乌云压顶
'''
第一日长阳，第二日开盘价高于前一日最高价，同时收盘价处于前一日实体中部以下，预示着股票下跌
'''
df['dark_cloud'] = talib.CDLDARKCLOUDCOVER(df['open'].values,
                                           df['high'].values, df['low'].values,
                                           df['close'].values)

pattern = df[(df['dark_cloud'] == 100) | (df['dark_cloud'] == -100)]

print(pattern)
