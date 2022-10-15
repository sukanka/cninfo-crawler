#!/usr/bin/python
import os
import requests as r
import json
import logging
from datetime import datetime
from src.constants import UA
from src.constants import DICT
logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='{}.log'.format(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    filemode='w',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


class DownloadMeta:
    def __init__(self, prefix: int, stockid: str, name: str, start_date: str, title: str, url: str, end_date=None) -> None:
        '''
        prefix: 序号，
        stockid: 股票代码
        name: 公司名称
        date: 公告日期
        title: 公告标题
        url: 公告下载链接
        '''
        self.title = title.replace('/', "每")
        self.stockid = stockid
        self.name = name.replace('/', "每")
        self.start_date = start_date
        self.url = url
        self.prefix = prefix
        if end_date == None:
            end_date = start_date
        self.end_date = end_date

    def __repr__(self) -> str:
        s=f'''
            "stockid" : {self.stockid},
            "name" : {self.name},
            "start_date" : {self.start_date},
            "end_date" : {self.end_date},
            "prefix" : {self.prefix},
            "url": {self.url}
            "title" : {self.title}
        '''
        return s
    def download(self, dir="assets") -> None:
        file_name = "{}-{}-{}-{} to {}-{}.pdf".format(
            self.prefix, self.name, self.stockid, self.start_date, self.end_date, self.title)
        download_path = os.path.join(dir, file_name)
        file = r.get(self.url, allow_redirects=True)
        if file.status_code != 200:
            logging.error("{} 下载失败".format(file_name))
        if not os.path.exists(download_path):
            with open(download_path, "wb") as f:
                f.write(file.content)
            logging.info("{} successfully downloaded".format(file_name))
        else:
            logging.info("{} already downloaded".format(file_name))


def get_announce_urls(stockid: str, start_date: str, end_date: str = None, prefix: int = 0, ua=UA.random) -> list[DownloadMeta]:
    '''获取公告下载链接。
    stockid: 股票代码，
    date: 公告日期： YYYY-MM-DD
    '''
    name = DICT[stockid]['zwjc']  # 中文简称
    org_id = DICT[stockid]['orgId']
    query_url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    download_url = "http://static.cninfo.com.cn"
    downloads = []
    if end_date == None:
        end_date = start_date
    data = {
        "pageNum":    "1",
        "pageSize":    "30",
        "column":    "szse",
        "tabName":    "fulltext",
        "plate": "",
        "stock": "{},{}".format(stockid, org_id),
        "searchkey": "",
        "secid": "",
        "category": "",
        "trade": "",
        "seDate": "{}~{}".format(start_date, end_date),
        "sortName": "",
        "sortType": "",
        "isHLtitle": "true",
    }
    c = r.post(query_url, data=data, headers={'user-agent': ua})
    if c.status_code == 200:
        json_c = json.loads(c.text)
        announces = json_c['announcements']
        if announces == None:
            logging.warning(
                "No download urls found for  {}-{}-{}-{} to {}".format(
                    prefix, name, stockid, start_date, end_date)
            )
            return downloads
        announces_num = len(announces)
        if announces_num > 0:
            for i in range(announces_num):
                announce = announces[i]
                download_meta = DownloadMeta(
                    prefix,
                    announce['secCode'],
                    announce['secName'],
                    start_date,
                    announce['announcementTitle'],
                    download_url+'/'+announce['adjunctUrl']
                )
                downloads.append(download_meta)
        logging.info(
            "successfully add download urls for {}-{}-{}-{}-{}".format(
                prefix, name, stockid, start_date, end_date)
        )
        return downloads
    else:
        logging.error(
            "failed to get download urls for {}-{}-{}-{}".format(
                prefix, name, stockid, start_date, end_date)
        )


if __name__ == '__main__':
    day = datetime.strptime("20160701", '%Y%m%d')
    urls = get_announce_urls("300409",  day.strftime("%Y-%m-%d"))
    print(urls)
    for url in urls:
        url.download()
