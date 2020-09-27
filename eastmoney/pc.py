

import re
import requests
from bs4 import BeautifulSoup as bs4
import csv
import json


# 爬取网页html
def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response = response.content.decode('utf-8')
    return response

# 将数据写入csv文件
def writeCSV(row, file):
    header = ['code','name']

    with open(file, 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(row)


def start(url):

    data_str = getHtml(url)
    re_result = re.findall(r'jQuery\d+\_\d+[(](.+?)[)];', data_str)

    if(re_result):
        obj_str = re_result[0]
        obj = json.loads(obj_str)

        # json解析
        json_str = json.dumps(obj)

        # 将 JSON 对象转换为 Python 字典
        json_dict = json.loads(json_str)

        print(type(json_dict['data']['diff']))

        list = []

        # # f12: 股票代码，f14:股票名称
        for stock_info in json_dict['data']['diff']:
            print(stock_info['f12'],stock_info['f14'])
            stock = (stock_info['f12'], stock_info['f14'])

            list.append(stock)



def main(urls):
    for url in urls:
        start(url)


if '__main__' == __name__:
    urls=[
        'http://58.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112404159415458446307_1601203368914&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1601203369049',
    ]

    main(urls)


