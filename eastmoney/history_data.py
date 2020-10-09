# -*- coding:UTF-8 -*-

import os
import requests
import csv
import time
import random
from lxml import etree

# proxyList = [
#     '115.221.247.208:9999',
#     '112.111.217.165:9999',
#     '61.130.181.231:20195',
#     '125.110.69.229:9000',
#     '123.163.27.150:9999',
# ]

userAgent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
]


def get_idx(max_num):
    num = random.randint(0, max_num)
    idx = num - 1

    if idx <= 0:
        idx = 0
    elif idx >= max_num - 1:
        idx = max_num - 1

    return idx


# def get_proxy():
#     """
#     随机获取代理ip
#     """
#     max_num = len(proxyList)
#     idx = get_idx(max_num)

#     proxy = proxyList[idx]
#     proxies = {
#         "http": "http://%(proxy)s/" % {'proxy': proxy},
#         "https": "http://%(proxy)s/" % {'proxy': proxy}
#     }

#     return proxies


def get_user_agent():
    """
    随机获取user_agent
    """
    max_num = len(userAgent)
    idx = get_idx(max_num)

    return userAgent[idx]


def get_code_prefix(code):
    """
    下载数据时code前缀
    上证：0，深证：1
    """
    if code[0:1] == '6':
        return '0'
    else:
        return '1'


class Download_HistoryStock(object):

    def __init__(self, code, save_file_path):
        # 下载后的保存路径名称
        self.save_file_path = save_file_path
        # 股票代码
        self.code = code
        # 前缀，上证0，深证1
        self.code_prefix = get_code_prefix(code)
        self.url = "http://quotes.money.163.com/trade/lsjysj_" + self.code + ".html"

        # 代理
        self.headers = {
            'User-Agent': get_user_agent()
        }
        # self.proxies = get_proxy()

    def parse_url(self):
        # response = requests.get(self.url, headers = self.headers, proxies= self.proxies)
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            return etree.HTML(response.content)

        print(response.status_code)
        return False

    def get_date(self, response):
        # 得到开始和结束的日期，默认 上市日 -- 今日
        start_date = ''.join(response.xpath(
            '//input[@name="date_start_type"]/@value')[0].split('-'))
        end_date = ''.join(response.xpath(
            '//input[@name="date_end_type"]/@value')[0].split('-'))

        return start_date, end_date

    def download(self, start_date, end_date):
        """
        下载文件流
        """
        download_url = "http://quotes.money.163.com/service/chddata.html?code=" + self.code_prefix + self.code + "&start=" + \
            start_date + "&end=" + end_date + \
            "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"

        data = requests.get(download_url, headers=self.headers)

        save_name = self.save_file_path + self.code + '.csv'
        f = open(save_name, 'wb')

        for chunk in data.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)

        print(self.code + ' 历史数据下载完成')

    def run(self):
        try:
            html = self.parse_url()
            if html is None:
                return

            start_date, end_date = self.get_date(html)
            self.download(start_date, end_date)

        except Exception as e:
            print('error : ', e)
            # print(html)

            pwd = os.path.split(os.path.realpath(__file__))[0]
            save_path = pwd + '/files/'
            with open(save_path + 'error.csv', 'a+') as f:
                csv_write = csv.writer(f)
                csv_write.writerow([self.code])


def download_file(code, save_path):
    # save_name = save_path + code + '.csv'

    # if not os.path.exists(save_name):
    download = Download_HistoryStock(code, save_path)
    download.run()
    time.sleep(10)


def start(source_path):

    pwd = os.path.split(os.path.realpath(__file__))[0]
    save_path = pwd + '/files/history/'

    # os.remove(pwd + '/files/error.csv')

    # 如果目标文件夹不存在，则新建
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(source_path, 'r') as f:
        reader = csv.reader(f)
        # reader = list(reader)

        for row in reader:
            code = row[0]
            download_file(code, save_path)


def get_unfinished():
    pwd = os.path.split(os.path.realpath(__file__))[0]
    save_path = pwd + '/files/history/'

    # 获取已下载的股票列表
    finished_arr = []
    finished = os.walk(save_path)
    for i, j, k in finished:
        for item in k:
            finished_arr.append(item[:-4])

    # 所有需要下载的文件列表
    all_arr = []
    with open(pwd + '/files/stock.py.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            all_arr.append(row[0])

    # 获取未下载的文件列表
    for i in finished_arr:
        all_arr.remove(i)

    print(all_arr)

    for code in all_arr:
        download_file(code, save_path)


if __name__ == '__main__':

    pwd = os.path.split(os.path.realpath(__file__))[0]
    cwdpath = os.path.abspath(os.path.dirname(pwd))

    err_path = cwdpath + '/err.csv'

    source_path = pwd + '/files/stock.py.csv'

    # start(err_path)
    start(source_path)

    # get_unfinished()
