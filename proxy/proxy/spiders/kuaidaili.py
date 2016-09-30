# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request

class KuaidailiSpider(scrapy.Spider):
    name = "kuaidaili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = (
        'http://www.kuaidaili.com/',
    )

    def start_requests(self):
        for i in xrange(1, 10):
            yield Request('http://www.kuaidaili.com/free/inha/%s/' % i, callback=self.parse)

    def parse(self, response):
        ip_records = response.xpath("//*[@id='list']//tbody//tr")
        for ip_record in ip_records:
            ip = ip_record.xpath('./td[1]/text()').extract_first()
            port = ip_record.xpath('./td[2]/text()').extract_first()
            proxy_type = ip_record.xpath('./td[4]/text()').extract_first().lower()
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

