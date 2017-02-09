# coding: utf-8
'''
@date: Feb 24, 2016
@author: alex.lin
'''
import datetime
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import DropItem
from house.items import SinaHouseItem, SinaHouseLayout


class SinaHouseSpider(CrawlSpider):
    """
    class:乐居房产爬虫: http://sh.leju.com/
    """

    name = 'leju'
    allowed_domains = ['leju.com', ]
    start_urls = ['http://sh.leju.com/', ]
    rules = [
        #  具体楼盘链接提取
        Rule(LinkExtractor(allow=(r'.*//house\.leju\.com/\w+\d+/(#wt_source=.*)?$')),
             callback='parse_house', follow=True),
        # 各个城市首页链接提取
        Rule(LinkExtractor(allow=(r'.*//\w+\.leju\.com/$'))),
        # 各个城市首页下的新房链接提取
        Rule(LinkExtractor(allow=(r'.*//house\.leju\.com/\w+/search/$'))),
        # 下一页链接
        Rule(LinkExtractor(allow=(r'.*//house\.leju\.com/\w+/search/\?page=\d+.*$'))),
    ]

    def parse_house(self, response):
        """
        func:提取楼盘信息
        :param response:
        :return: request
        """
        house = SinaHouseItem()
        house['create_time'] = datetime.datetime.now()
        house['source_id'] = int(
            re.search(r'.*?(?P<source_id>\d{1,})', response.url).groupdict('source_id')['source_id'])
        house['url'] = response.url
        house['cover_url'] = response.xpath(
            u"//ul[@class='b_list_02 clearfix conClassName']/li[1]//img/@lsrc").extract_first()
        house['cover_path'] = None
        # 去详情页获取楼盘详情
        detail_url = response.xpath(u"//ul[@class='z_main_menu']//a[contains(text(),'楼盘详情')]/@href").extract_first()
        if detail_url:
            yield scrapy.Request(detail_url, meta={'house': house}, callback=self.parse_house_detail)
        else:
            self.logger.info(u'此楼盘详情信息: %s', house['url'])

    def parse_house_detail(self, response):
        """
        func:获取楼盘详情
        :param response:
        :return: item/request
        """
        house = response.meta['house']
        house['name'] = response.xpath('//h1/text()').extract_first()
        house['price'] = response.xpath(
            "concat(//p[@class='price']/em/text(),//p[@class='price']/text()[2])").extract_first('未知').strip()

        house['open'] = response.xpath(
            u"//ul[@class='z_info_list clearfix']//li[contains(label, '开盘时间')]/text()").extract_first(u'待定').strip()
        house['check_in'] = response.xpath(
            u"//ul[@class='z_info_list clearfix']//li[contains(label, '入住时间')]/p/text()").extract_first(u'待定').strip()
        house['address'] = response.xpath(
            u"//ul[@class='z_info_list clearfix']//li[contains(label, '项目地址')]/p/text()").extract_first(u'未知').strip()
        house['lon_lat'] = ','.join([response.xpath('//script').re_first(".*?coordx='(\d+.\d+)'"), response.xpath(
            '//script').re_first(".*?coordy='(\d+.\d+)'.*")])
        house['developer'] = response.xpath(
            ur"//ul[@class='z_info_list clearfix']//li[contains(label,'\u5f00\u2002\u53d1\u2002\u5546\uff1a')]/p/text()").extract_first(
            u'未知').strip()
        house['property_company'] = response.xpath(
            u"//ul[@class='z_info_list clearfix']//li[contains(label, '物业公司')]/p/text()").extract_first(u'未知').strip()
        house['property_fee'] = response.xpath(
            u"//ul[@class='z_info_list z_info_list01 clearfix']//li[contains(label,'\u7269\u2002\u4e1a\u2002\u8d39\uff1a')]").extract_first(
            u'未知').strip()
        house['decoration'] = response.xpath(
            u"//ul[@class='z_info_list clearfix']//li[contains(label, '装修情况')]/text()").extract_first().strip()

        # 楼盘户型图首页
        houselayout_index_url = response.xpath('/html/body/div[1]/div[10]/ul/li[4]/a/@href').extract_first()

        if houselayout_index_url:
            yield scrapy.Request(url=houselayout_index_url, meta={"house": house},
                                 callback=self.parse_houselayout_index)
        else:
            self.logger.info(u'此楼盘无图片: %s', house['url'])
            yield house

    def parse_houselayout_index(self, response):
        """
        func:楼盘户型信息处理
        """
        house = response.meta["hosue"]
        house['layout_items'] = []
        houselayout_index_url = response.xpath(
            u"//div[@class='housingNav w']//li[contains(a,'户型图')]/a/@href").extract_first()
        if houselayout_index_url:
            self.logger.debug(u'楼盘图片首页: %s', houselayout_index_url)
            yield scrapy.Request(url=houselayout_index_url, meta={'house': house}, callback=self.parse_houselayout)
        else:
            self.logger.info(u'此楼盘无户型图片: %s', house['url'])
            yield house

    def parse_houselayout(self, response):
        """
        func:户型信息处理
        """
        house = response.meta['house_house']
        layout_records = response.xpath("//ul[@class='sFy03 clearfix']//li")
        for layout in layout_records:
            houselayout = SinaHouseLayout()
            houselayout['name'] = layout.xpath(".//div[@class='imgBox']/p/text()").extract_first(default=u'其他')
            img_url_tmp = layout.xpath('.//img/@src').extract_first()
            # 转换为大图的链接
            houselayout['img_url'] = '%s.jpg' % img_url_tmp[:(img_url_tmp.index('mk7') + 3)]
            houselayout['img_path'] = None
            houselayout['area'] = layout.xpath("./p[1]/em/text()").extract_first(default=0)
            houselayout['price'] = '%s%s' % (
                layout.xpath('./p[2]/em/text()').extract_first(''), layout.xpath('./p[2]/text()[2]').extract_first(''))
            house['layout_items'].append(dict(houselayout))

        # 部分户型图有分页, 如: http://data.house.sina.com.cn/sc127009/huxing/#wt_source=data6_tpdh_hxt       
        next_url = response.xpath(u"//div[@class='sPageBox']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url:
            self.logger.debug(u'进入楼盘户型图下一页: %s', next_url)
            yield scrapy.Request(url=next_url, meta={'house': house,}, callback=self.parse_houselayout)
        else:
            self.logger.info(u'此楼盘链接处理完毕: %s', house['url'])
            yield house
