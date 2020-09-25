

import re
import requests
from bs4 import BeautifulSoup as bs4
import csv


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

    html_doc = getHtml(url)

    soup = bs4(html_doc, 'html.parser')

    stockListWrapper = soup.find("div", id="ctrlfscont")
    stockListHtml = stockListWrapper.find_all('a')

    stockList = []

    for li in stockListHtml:
        stock = re.findall(r"(.{1,})[(](\d{6})[)]", li.contents[0])[0]
        stockList.append((stock[1],stock[0]))


    file_name = url[url.find('_')+1:].split('.')[0]
    file_name = file_name + '.csv'

    print(file_name + ' ' + str(len(stockList)))
    writeCSV(stockList, file_name)


def main(urls):
    for url in urls:
        start(url)


if '__main__' == __name__:
    urls=[
        'https://www.banban.cn/gupiao/list_sh.html',
        'https://www.banban.cn/gupiao/list_sz.html',
        'https://www.banban.cn/gupiao/list_cyb.html'
    ]

    main(urls)


