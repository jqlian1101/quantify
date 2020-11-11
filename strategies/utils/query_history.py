# -*- coding:UTF-8 -*-

# 接口文档说明
# http://baostock.com/baostock/index.php/A%E8%82%A1K%E7%BA%BF%E6%95%B0%E6%8D%AE

import baostock as bs
from numpy.lib.function_base import delete
import pandas as pd
import os

default_bs_cols = ["date","code","open","high","low","close","preclose","volume","amount","adjustflag","turn","tradestatus","pctChg","isST"]

class QueryHistory:
    def __init__(self, code, date, cols=default_bs_cols, frequency='d', adjustflag='3'):
        self.code = code                # 要查询的股票代码
        self.start_date = date[0]       # 开始时间
        self.end_date = date[1]         # 结束时间
        self.frequency = frequency      # 数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
        self.adjustflag = adjustflag    # 复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权。
        self.bs_cols = cols

    def query_from_bs(self):
        bs.login()
        # lg = bs.login()
        # 显示登陆返回信息
        # print('login respond error_code:'+lg.error_code)
        # print('login respond  error_msg:'+lg.error_msg)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(self.code, ','.join(self.bs_cols),
            start_date=self.start_date, end_date=self.end_date,
            frequency=self.frequency, adjustflag=self.adjustflag)


        # print('query_history_k_data_plus respond error_code:' + rs.error_code)
        # print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())

        result = pd.DataFrame(data_list, columns=rs.fields)

        # result = result.set_index('date', drop=True, append=False, inplace=False, verify_integrity=False)
        # result.index = pd.DatetimeIndex(result.index)  # 转换为时间戳索引

        result.index = pd.DatetimeIndex(result['date'])
        del result['date']

        for key in self.bs_cols:
            if key != 'date' and key != 'code':
                result[key] = pd.to_numeric(result[key])

        #### 登出系统 ####
        bs.logout()

        return result

    def query_from_local(self):
        pwd = os.path.realpath(__file__)
        work_dir = os.path.dirname(os.path.dirname(os.path.dirname(pwd)))

        code = self.code.split('.')[1]
        history_dir = os.path.join(work_dir,'files/history',self.code.split('.')[1] + '.csv')

        df = pd.read_csv(history_dir, index_col=0)
        df['code'] = code

        df.index = pd.DatetimeIndex(df.index)

        return df[['code','open','high','low','close','preclose','chg', 'pctChg', 'turn', 'volume', 'amount', 'tcap', 'mcap']]



if '__main__' == __name__:
    query_history = QueryHistory('sh.600000',('2019-1-1', '2020-1-1'))
    df = query_history.query_from_local()

    print(df.index)

