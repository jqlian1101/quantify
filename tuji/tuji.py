# -*- coding:UTF-8 -*-

import requests
from lxml import etree
import re
import os
import random
import time
import json


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


def get_user_agent():
    """
    随机获取user_agent
    """
    max_num = len(userAgent)
    idx = get_idx(max_num)

    return userAgent[idx]


def get_headers():
    return {
        'User-Agent': get_user_agent()
    }


def gethtml(url):  # 获取网页源码
    time.sleep(5)

    r = requests.get(url, headers=get_headers())
    r.encoding = 'utf-8'
    return r.text


def mkdir(path):  # 创建文件夹
    pwd = os.path.split(os.path.realpath(__file__))[0]
    save_path = pwd + '/files/'

    path = path.strip()
    folder_path = save_path + path

    isExists = os.path.exists(folder_path)
    if not isExists:
        os.makedirs(folder_path)

    return folder_path


def downPic(url, savepath):  # 下载图片
    picname = url.split('/')[-1]

    file_path = savepath + '/' + picname
    isExists = os.path.exists(file_path)

    if not isExists:
        picdata = requests.get(url, headers=get_headers())
        with open(file_path, mode='wb') as file:
            file.write(picdata.content)


def analysis_detail_page(html):
    """
    解析详情页
    """
    ehtml = etree.HTML(html)
    urls = ehtml.xpath('//*[@class="content"]/img/@src')

    explain_html = ehtml.xpath('//*[@class="tuji"]/p')

    detail = {}

    for i in range(len(explain_html)):
        item = explain_html[i]

        p_text = item.xpath('text()')[0]
        p_text = p_text.strip().split('：')
        p_type = p_text[0]

        if '拍摄机构' == p_type:
            organ_a = item.xpath('a')[0]
            organ = (organ_a.xpath('text()')[0], organ_a.xpath('@href')[0])

            detail['organ'] = organ

        elif '相关编号' == p_type:
            no = p_text[1]
            no = no.strip()     # 去除左右空格

            detail['no'] = no

        elif '图片数量' == p_type:
            num = p_text[1]
            num = num.strip()     # 去除左右空格
            num = num[:-1]

            detail['num'] = int(num)

        elif '发行日期' == p_type:
            date = p_text[1]
            date = date.strip()

            detail['date'] = date

        # elif '出镜模特' == p_type:
        #     models = item.xpath('a')
        #     _models = []

        #     for m in models:
        #         model_href = m.xpath('@href')[0]
        #         model_name = m.xpath('text()')[0]
        #         _models.append((model_name, model_href))

        #     model_desc = item.xpath('text()')

        #     detail['models'] = _models
        #     detail['model_desc'] = model_desc[len(model_desc) - 1].strip()

    # 说明
    shuoming = ehtml.xpath(
        '//*[@class="tuji"]/div[@class="shuoming"]/p/text()')
    if shuoming and len(shuoming) > 0:
        shuoming = shuoming[0]
    else:
        shuoming = ''

    # 获取页数
    pages = ehtml.xpath('//*[@id="pages"]/*')
    cur_page = ehtml.xpath('//*[@id="pages"]/span/text()')[0]
    total_page = pages[-2].xpath('text()')[0]

    detail['cur_page_urls'] = urls
    detail['desc'] = shuoming
    detail['total_page'] = int(total_page)
    detail['cur_page'] = int(cur_page)

    return detail


def analysis_list_page(html):
    """
    解析列表页
    """

    ehtml = etree.HTML(html)
    li = ehtml.xpath('//*[@class="hezi"]//li')

    photo_list = []

    for item in li:
        cur_info = item.xpath('*')

        # 地址
        atlas_url = cur_info[0].xpath('@href')[0]

        # 图片数量
        num = cur_info[1].xpath('text()')[0]
        if num:
            num = num[:-1]
        else:
            num = 0

        # 所属机构
        organ_a = cur_info[2].xpath('a')[0]
        organ = (organ_a.xpath('text()')[0], organ_a.xpath('@href')[0])

        # 模特
        model_list = cur_info[3].xpath('a')
        models = []
        for model in model_list:
            model = (model.xpath('text()')[0], model.xpath('@href')[0])
            models.append(model)

        # 标签
        tag_list = cur_info[4].xpath('a')
        tags = []
        for tag in tag_list:
            cur = (tag.xpath('text()')[0], tag.xpath('@href')[0])
            tags.append(cur)

        # 标题
        title = cur_info[5].xpath('a')
        if len(title) > 0:
            title = {
                'href': title[0].xpath('@href')[0],
                'desc': title[0].xpath('text()')[0],
            }
        else:
            title = {}

        li_info = {
            'title': title,
            'atlas_url': atlas_url,
            'num': int(num),
            'organ': organ,
            'models': models,
            'tags': tags
        }

        photo_list.append(li_info)

    # 获取页数
    pages = ehtml.xpath('//*[@id="pages"]/*')
    cur_page = ehtml.xpath('//*[@id="pages"]/span/text()')[0]
    total_page = pages[-2].xpath('text()')[0]

    return {
        'cur_page_atlas': photo_list,
        'cur_page': int(cur_page),
        'total_page': int(total_page),
    }


def save_altas_info(info, folder_path):
    save_name = folder_path + '/info.json'
    is_have = os.path.exists(save_name)

    datas = {**info}
    if is_have:
        with open(save_name, 'r') as f:
            strF = f.read()

            if len(strF) > 0:
                datas = json.loads(strF)

            datas = {**datas, **info}

    with open(save_name, 'w') as f:
        json.dump(datas, f, ensure_ascii=False)


def download_imgs(page_url, folder_path):
    """
    下载当前页图片
    返回当前页详情
    """
    html = gethtml(page_url)
    detail = analysis_detail_page(html)

    cur_page_urls = detail['cur_page_urls']

    for page_url in cur_page_urls:
        downPic(page_url, folder_path)

    # 保存当前图集对基本信息
    save_altas_info({
        'no': detail.get('no'),
        'desc': detail.get('desc'),
        'date': detail.get('date'),
        # 'models': detail['models'],
        # 'tags': detail['tags']
    }, folder_path)

    return detail


def get_list_page(url, total_list_page):
    for i in range(total_list_page):
        page_idx = i + 1
        page_url = url + str(page_idx) + '.html'

        print('第%d页开始下载，共%d页' % (page_idx, total_list_page))

        if 1 == page_idx:
            page_url = url

        page_html = gethtml(page_url)
        page_info = analysis_list_page(page_html)

        cur_page_atlas = page_info['cur_page_atlas']

        for altas in cur_page_atlas:
            # 创建文件夹
            desc = altas['title']['desc']
            folder_path = mkdir(desc)

            # 保存当前图集对基本信息
            save_altas_info({
                'title': altas['title']['desc'],
                'num': altas['num'],
                'organ': altas['organ'],
                'models': altas['models'],
                'tags': altas['tags']
            }, folder_path)

            # 获取图集详情
            atlas_url = altas['atlas_url']

            # 第一页
            # 下载当前页图片
            # 返回当前页信息
            detail = download_imgs(atlas_url, folder_path)

            # 获取页码信息
            total_page = detail['total_page']

            print(altas['title']['desc'], '第1页下载完成，共%d页' % (total_page))

            # 其余页码
            for cur_page in range(2, total_page + 1):
                _url = atlas_url + '/' + str(cur_page) + '.html'
                download_imgs(_url, folder_path)

                print(altas['title']['desc'], '第%d页下载完成，共%d页' %
                      (cur_page, total_page))


def start(urls):
    for url in urls:
        html = gethtml(url)
        cur_url_info = analysis_list_page(html)

        total_page = cur_url_info['total_page']
        get_list_page(url, total_page)


if __name__ == '__main__':
    urls = [
        'https://www.tujigu.com/zhongguo/',
        'https://www.tujigu.com/hanguo/',
        "https://www.tujigu.com/riben/",

    ]
    start(urls)

    # pwd = os.path.split(os.path.realpath(__file__))[0]
    # save_path = pwd + '/files/'

    # url = 'https://www.tujigu.com/zhongguo/'
    # html = gethtml(url)
    # list_info = analysis_list_page(html)
    # print(list_info)

    # folder_name = list_info['cur_page_atlas'][0]['title']['desc']

    # mkdir(save_path + '/' + folder_name)

    # url = 'https://www.tujigu.com/a/7339/'
    # # url = 'https://www.tujigu.com/a/18962/'
    # html = gethtml(url)
    # detail = analysis_detail_page(html)
    # print(detail)

    # urls = detail['cur_page_urls']

    # for url in urls:
    #     downPic(url, save_path)

    # altas = {'title': {'href': 'https://www.tujigu.com/a/7339/', 'desc': 'test'}, 'atlas_url': 'https://www.tujigu.com/a/7339/', 'num': 51, 'organ': ('秀人网', 'https://www.tujigu.com/x/59/'), 'models': [(
    #     '许诺', 'https://www.tujigu.com/t/296/')], 'tags': [('比基尼', 'https://www.tujigu.com/s/49/')]}

    # # 创建文件夹
    # desc = altas['title']['desc']
    # folder_path = mkdir(desc)

    # save_altas_info({
    #     'title': altas['title']['desc'],
    #     'num': altas['num'],
    #     'organ': altas['organ'][0],
    #     'models': altas['models'],
    #     'tags': altas['tags']
    # }, folder_path)

    # time.sleep(10)
    # save_altas_info({
    #     'no': '001',
    #     'date':'2020-20-20',
    #     'desc':'aaaa'
    # }, folder_path)
