# coding:utf-8
# author:alex lin

import re

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from sinahouse.items import SinaHouseItem, SinaHouseLayout
from sinahouse import settings


class SinaHouseSpider(CrawlSpider):
    """新浪房产爬虫: http://sh.house.sina.com.cn/"""
    name = 'sinahouse'
    allowed_domains = ['house.sina.com.cn']
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
        item = SinaHouseItem()
        item['source_id'] = settings.SOURCE
        item['name'] = response.xpath('//h1/text()').extract_first()
        item['price'] = response.xpath("//*[@id='callmeBtn']/ul/li[1]/em[1]/text()").extract_first(default=u'未知').strip()
        item['url'] = response.url
        item['open_date'] = '-'.join(re.findall('(\d+)',response.xpath(u"//*[@id='callmeBtn']/ul/li[4]/span[2]/text()").extract_first(default=u'待定').strip()))
        item['checkin_date'] = '-'.join(re.findall('(\d+)',response.xpath(u'(//*[@id="callmeBtn"]//div[@title])[2]/@title').extract_first(default=u'待定')))
        item['address'] = response.xpath(u'//*[@id="callmeBtn"]/ul/li[2]/span[2]/text()').extract_first(default=u'未知').strip()
        item['longtitude_latitude'] = ','.join([response.xpath('//script').re_first(".*?coordx='(\d+.\d+)'"), response.xpath('//script').re_first(".*?coordy='(\d+.\d+)'.*")])
        item['developer'] = response.xpath(u"//div[@class='info wm']/ul/li[3]/text()").extract_first(default=u'未知').strip()
        item['property_company'] = response.xpath(u"//li[contains(span,'物业公司')]/text()").extract_first(default=u'未知').strip()
        item['decoration'] = response.xpath("//div[@class='info wm']/ul/li[12]/text()").extract_first(default=u'未知').strip()
        item['cover_info'] = {'url': response.xpath("//*[@id='con_tab1_con_4']/a/img/@lsrc").extract_first(),}
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
            houselayout['img_info'] = {'url': '%s.jpg' % img_url_tmp[:(img_url_tmp.index('mk7')+3)],}
            houselayout['area'] = layout.xpath("./p[1]/em/text()").extract_first(default=0)
            item['layout_items'].append(dict(houselayout))
        
        # 部分户型图有分页, 如: http://data.house.sina.com.cn/sc127009/huxing/#wt_source=data6_tpdh_hxt       
        next_url = response.xpath(u"//div[@class='sPageBox']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url:
            self.logger.debug(u'进入楼盘户型图下一页: %s', next_url )
            yield scrapy.Request(url=next_url, meta={'house_item': item,},callback=self.parse_houselayout)
        else:
            self.logger.info(u'此楼盘链接处理完毕: %s', item['url'])
            yield item
    
    
