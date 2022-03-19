from scrapy.pipelines.files import FilesPipeline
from scrapy import Request

class ReportDownloaderPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return Request(item['durl'], meta={'title':item['title']})

    def file_path(self, request, response=None, info=None):
        name = request.meta['title']
        return name