# Python Scrapy 招股说明书和问询函爬虫

## 介绍

数据来自“东方财富网”，有些上市年份久远的公司没有问询函，只有招股书。

![dfcfw1](https://github.com/sqwqwqw1/IPO_crawler/blob/main/dfcfw1.png)

需要安装Python，还有其他一些模块：

1. pip install scrapy
2. pip install panas
3. pip install requests

## 使用说明

下载此文件，修改其中的“股票代码.py”，只需要改动“代码”这一列，名称那一列可有可无。

![dfcfw2](https://github.com/sqwqwqw1/IPO_crawler/blob/main/dfcfw2.png)

然后直接运行start.py即可，会在解压的目录生成一个“下载的报告”文件夹，效果如下：

![dfcfw3](https://github.com/sqwqwqw1/IPO_crawler/blob/main/dfcfw3.png)

