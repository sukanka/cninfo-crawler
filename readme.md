# CNINFO CRAWLER

[巨潮资讯](http://www.cninfo.com.cn/new/index) 爬虫，自动下载上市公司公告

## 使用说明

### 安装依赖

```shell
pip install -r requirements.txt
```

### 用法

读取 `aux/并购公告下载.xls` 的每一行并根据 `'序号', 'stockid', "首次披露日"` 下载`首次披露日`的公告。

从序号等于 `start` 开始下载，不输入 `start` 时默认下载所有 (`start=0`)。会自动跳过已经下载的文件

```shell
python main.py [start]
```

## TODO LIST

- 使用 IP 代理池
- 加入多线程支持

## 声明

保留所有权利，仅供学习研究使用。
