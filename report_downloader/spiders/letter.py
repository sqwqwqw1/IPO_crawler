import scrapy,json,requests,os
import pandas as pd
from numpy import random
from datetime import datetime
from report_downloader.items import ReportDownloaderItem

class LetterSpider(scrapy.Spider):
    name = 'letter'
    allowed_domains = ['eastmoney.com']

    def start_requests(self):
        # 读取股票列表
        index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'股票代码.xlsx')
        df = pd.read_excel(index_path,dtype={'代码':str})
        code_list = df['代码']
        for code in code_list:
            # 设置api网址
            baseurl = 'https://np-anotice-stock.eastmoney.com/api/security/ann?'
            # 获取当前时间戳
            ts = int(datetime.now().timestamp()*1000)
            cb = 'jQuery11230{}{}_{}'.format(random.randint(100000000,499999999),random.randint(10000000,99999999),ts)
            # 设置请求表单
            formdata = {
                'cb':cb,
                'sr':'-1',
                'page_size':'50',
                'page_index':1,
                'ann_type':'A',
                'client_source':'web',
                'stock_list':code,
                'f_node':'0',
                's_node':'0',
            }
            # 发起一次请求，获取总页数
            url = '{}{}'.format(baseurl,'&'.join(['{}={}'.format(x[0],x[1]) for x in formdata.items()]))
            r = requests.get(url,data=formdata)
            r = json.loads(r.text.replace('{}('.format(cb),'').replace(')',''))
            finalpage = r['data']['total_hits']//50

            # 只遍历最后三页，每页查看50条文件列表
            for page in range(finalpage-2,finalpage+2):
                # 重设时间戳
                ts = int(datetime.now().timestamp()*1000)
                cb = 'jQuery11230{}{}_{}'.format(random.randint(100000000,499999999),random.randint(10000000,99999999),ts)
                formdata = {
                    'cb':cb,
                    'sr':'-1',
                    'page_size':'50',
                    'page_index':page,
                    'ann_type':'A',
                    'client_source':'web',
                    'stock_list': code,
                    'f_node':'0',
                    's_node':'0',
                }
                # 发起请求
                url = '{}{}'.format(baseurl,'&'.join(['{}={}'.format(x[0],x[1]) for x in formdata.items()]))
                yield scrapy.Request(url,meta={'cb':cb},callback=self.get_list,dont_filter=True)


    def get_list(self, response):
        li = json.loads(response.text.replace('{}('.format(response.meta['cb']),'').replace(')',''))['data']['list']
        for one in li:
            name = one['title'].replace('\\',' ').replace('/',' ')
            # 回复意见
            if ('发行人' in one['title']) and ('回复意见' in one['title']) and ('落实' not in one['title']):
                title = '{}_{}_{}.pdf'.format(one['codes'][0]['stock_code'],one['codes'][0]['short_name'],name)
                durl = 'https://pdf.dfcfw.com/pdf/H2_{}_1.pdf'.format(one['art_code'])
                item = ReportDownloaderItem(title=title,durl=durl)
                yield item

            # 招股说明书
            if ('招股说明书' in one['title']):
                title = '{}_{}_{}.pdf'.format(one['codes'][0]['stock_code'],one['codes'][0]['short_name'],name)
                durl = 'https://pdf.dfcfw.com/pdf/H2_{}_1.pdf'.format(one['art_code'])
                item = ReportDownloaderItem(title=title,durl=durl)
                yield item
