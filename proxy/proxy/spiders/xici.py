# coding: utf-8
'''
@date: 2016-09-28
@author: alex.lin
'''

from scrapy.spiders import Spider
from scrapy.http.request import Request



class XiciSpider(Spider):
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/']

    def start_requests(self):
        for i in xrange(1, 10):
            yield Request('http://www.xicidaili.com/nn/%s' % i, callback=self.parse)
        
    def parse(self, response):
        ip_records = response.xpath("//*[@id='ip_list']//tr")
        for ip_record in ip_records[1:]:
            ip = ip_record.xpath('./td[2]/text()').extract_first()
            port = ip_record.xpath('./td[3]/text()').extract_first()
            proxy_type = ip_record.xpath('./td[6]/text()').extract_first().lower()
            if proxy_type == 'http':
                yield Request('http://www.163.com/',dont_filter=True, 
                              meta={'item': {proxy_type: '%s:%s' % (ip, port),},
                                    'proxy':'%s://%s:%s' % (proxy_type, ip, port),
                                    'dont_retry': True,
                                    },
                              callback=self.examined_item)
    
    def examined_item(self,response):
        item = response.meta['item']
        yield item