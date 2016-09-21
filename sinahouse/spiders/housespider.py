# coding: utf-8
'''
@date: Feb 24, 2016
@author: alex.lin
'''
import re
import datetime

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from sinahouse.items import SinaHouseItem, SinaHouseLayout


class SinaHouseSpider(CrawlSpider):
    """
    class:新浪房产爬虫: http://sh.house.sina.com.cn/
    """
    
    name = 'sinahouse'
    allowed_domains = ['house.sina.com.cn',]
    start_urls = ['http://data.house.sina.com.cn/sc/search/?keyword=&charset=utf8',]
    rules = [
            Rule(LinkExtractor(allow = ('.*\.cn/\w+\d+/#wt_source.*?bt.*')), callback='parse_house', follow=False), #  具体楼盘链接提取
            Rule(LinkExtractor(allow = ('^http://data.house.sina.com.cn/\w+/search$'))), # 各个城市链接提取
            Rule(LinkExtractor(allow = ('^http://data.house.sina.com.cn/\w+/search/\?bcity.*'))), # 各个省份下有其他城市的链接提取
            Rule(LinkExtractor(allow = ('/\w+/search-\d*/.*'))), # 下一页链接
            ]

    def parse_house(self, response):
        """
        func:提取楼盘信息
        """
#         from scrapy.shell import inspect_response
#         inspect_response(response, self)
        item = SinaHouseItem()
        item['create_time'] = datetime.datetime.now()
        item['source_id'] = int(re.search(r'.*?(?P<source_id>\d{1,})', response.url).groupdict('source_id')['source_id'])
        item['name'] = response.xpath('//h1/text()').extract_first()
        item['price'] = ''.join(response.xpath("//*[@id='callmeBtn']/ul/li[1]/em[1]/text() | //*[@id='callmeBtn']/ul/li[1]/em[2]/text() ").extract()) or u'未知'
        item['url'] = response.url
        item['open_date'] = '-'.join(re.findall('(\d+)',response.xpath(u"//*[@id='callmeBtn']/ul/li[4]/span[2]/text()").extract_first(default=u'待定').strip()))
        item['checkin_date'] = '-'.join(re.findall('(\d+)',response.xpath(u'(//*[@id="callmeBtn"]//div[@title])[2]/@title').extract_first(default=u'待定')))
        item['address'] = response.xpath(u'//*[@id="callmeBtn"]/ul/li[2]/span[2]/text()').extract_first(default=u'未知').strip()
        item['lon_lat'] = ','.join([response.xpath('//script').re_first(".*?coordx='(\d+.\d+)'"), response.xpath('//script').re_first(".*?coordy='(\d+.\d+)'.*")])
        item['developer'] = response.xpath(u"//div[@class='info wm']/ul/li[3]/text()").extract_first(default=u'未知').strip()
        item['property_company'] = response.xpath(u"//li[contains(span,'物业公司')]/text()").extract_first(default=u'未知').strip()
        item['property_manage_fee'] = response.xpath("//div[@class='info wm']/ul/li[7]/text()").extract_first(default=u'未知').strip()
        item['decoration'] = response.xpath("//div[@class='info wm']/ul/li[12]/text()").extract_first(default=u'未知').strip()
        item['cover_url'] = response.xpath("//*[@id='con_tab1_con_4']/a/img/@lsrc").extract_first()
        item['cover_path'] = None
        # 楼盘户型图首页
        houselayout_index_url = response.xpath('/html/body/div[1]/div[10]/ul/li[4]/a/@href').extract_first()

        if houselayout_index_url:
            yield scrapy.Request(url=houselayout_index_url, meta={"house_item": item}, callback=self.parse_houselayout_index)
        else:
            self.logger.info(u'此楼盘无图片: %s', item['url'])
            yield item
    
    def parse_houselayout_index(self,response):
        """
        func:楼盘户型信息处理
        """
        item = response.meta["house_item"]
        item['layout_items'] = []
        houselayout_index_url = response.xpath(u"//div[@class='housingNav w']//li[contains(a,'户型图')]/a/@href").extract_first()
        if houselayout_index_url:
            self.logger.debug(u'楼盘图片首页: %s', houselayout_index_url )
            yield scrapy.Request(url=houselayout_index_url, meta={'house_item':item}, callback=self.parse_houselayout)
        else:
            self.logger.info(u'此楼盘无户型图片: %s', item['url'])
            yield item
            
    def parse_houselayout(self,response):
        """
        func:户型信息处理
        """
        item = response.meta['house_item']
        layout_records = response.xpath("//ul[@class='sFy03 clearfix']//li")
        for layout in layout_records:
            houselayout = SinaHouseLayout()
            houselayout['name'] = layout.xpath(".//div[@class='imgBox']/p/text()").extract_first(default=u'其他')
            img_url_tmp = layout.xpath('.//img/@src').extract_first()
            # 转换为大图的链接
            houselayout['img_url'] = '%s.jpg' % img_url_tmp[:(img_url_tmp.index('mk7')+3)]
            houselayout['img_path'] = None
            houselayout['area'] = layout.xpath("./p[1]/em/text()").extract_first(default=0)
            houselayout['price'] = '%s%s' %(layout.xpath('./p[2]/em/text()').extract_first(''), layout.xpath('./p[2]/text()[2]').extract_first(''))
            item['layout_items'].append(dict(houselayout))
        
        # 部分户型图有分页, 如: http://data.house.sina.com.cn/sc127009/huxing/#wt_source=data6_tpdh_hxt       
        next_url = response.xpath(u"//div[@class='sPageBox']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url:
            self.logger.debug(u'进入楼盘户型图下一页: %s', next_url )
            yield scrapy.Request(url=next_url, meta={'house_item': item,},callback=self.parse_houselayout)
        else:
            self.logger.info(u'此楼盘链接处理完毕: %s', item['url'])
            yield item
    
    
