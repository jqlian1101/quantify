import re
import os
import requests
from bs4 import BeautifulSoup as bs4
import csv
import json
import math
import time

# http://quote.eastmoney.com/center/gridlist.html#hs_a_board

class EastMoney:

    def __init__(self):
        self.current = 1
        self.page_size = 20
        self.total_page = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
        }

    def get_url(self, page):
        """
        获取url
        """
        return 'http://58.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112404159415458446307_1601203368914&pn=%d&pz=%d&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14&_=1601203369049'%(page, self.page_size)


    def get_html(self, url):
        """
        获取请求网络数据
        """
        response = requests.get(url, headers = self.headers)
        response = response.content.decode('utf-8')

        return response


    def fetch(self, page):
        url = self.get_url(page)

        html_doc = self.get_html(url)
        self.current = self.current + 1

        return html_doc

    def writeBefore(self, stockList):
        _list = []

        for stock_info in stockList:
            stock = (stock_info['f12'], stock_info['f14'])

            _list.append(stock)

        return _list


    def writeCSV(self, stockList, file):
        """
        将数据写入csv文件
        """

        row = self.writeBefore(stockList)

        if os.path.isfile(file):
            # 如果文件存在，直接写入
            with open(file, 'a+', encoding='utf8') as f:
                writer = csv.writer(f)
                writer.writerows(row)

        else:
            # 如果文件不存在，则添加header row
            header = ['code','name']
            with open(file, 'a+', encoding='utf8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(row)


    def analytic_data(self,data_str):
        """
        解析返回的数据
        """

        re_result = re.findall(r'jQuery\d+\_\d+[(](.+?)[)];', data_str)

        if(re_result):
            obj_str = re_result[0]
            obj = json.loads(obj_str)

            # json解析
            json_str = json.dumps(obj)

            # 将 JSON 对象转换为 Python 字典
            json_dict = json.loads(json_str)

            total = json_dict['data']['total']
            curList = json_dict['data']['diff']

            return total, curList


    def init_total(self):
        url = self.get_url(1)
        html_doc = self.get_html(url)
        total, list = self.analytic_data(html_doc)

        total_page = math.ceil(total / self.page_size)

        self.total_page = total_page


    def start(self):
        if not self.total_page:
            self.init_total()

        for page in range(self.total_page):
            data_str = self.fetch(page + 1)
            total, stockList = self.analytic_data(data_str)

            file_path = os.path.abspath(__file__)
            file_name = file_path.split('/')
            print(file_name)

            self.writeCSV(stockList, file_name[-1] + '.csv')
            time.sleep(100)     # 休眠100秒



if '__main__' == __name__:

    east = EastMoney()
    east.start()


