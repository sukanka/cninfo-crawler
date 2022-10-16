#!/usr/bin/python
import pandas
import re
from datetime import datetime
from src.download_file import get_announce_urls

df = pandas.read_excel("auxiliary/并购公告下载.xls")


def buyer2stockid(s: str) -> str:
    z = re.search(r'(\d+)\.(SH|SZ)', s).groups()[0]
    return z


def parsedate(s: str) -> str:
    day = datetime.strptime(str(s), '%Y%m%d')
    return day.strftime("%Y-%m-%d")


# 生成 股票代码
df['stockid'] = df['buyer'].map(buyer2stockid)
df["首次披露日"] = df['首次披露日'].map(parsedate)
# 只要这三个就行
df = df[['序号', 'stockid', "首次披露日"]]


def start_download(start=0):
    '''从 序号start 开始，默认取0
    '''
    for index, row in df.iterrows():
        if row['序号'] >= start:
            urls = get_announce_urls(row['stockid'],  row['首次披露日'], prefix=row['序号'])
            for url in urls:
                url.download()


if __name__ == "__main__":
    start_download(0)
