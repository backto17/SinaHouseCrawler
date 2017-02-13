# coding: utf-8
"""
@date: Feb 24, 2016
@author: alex.lin
"""
import datetime
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from house.items import SinaHouseItem, SinaHouseLayout

class SinaHouseSpider(CrawlSpider):
    """
    class:乐居房产爬虫: http://sh.leju.com/
    """

    name = 'leju'
    allowed_domains = ['leju.com', ]
    start_urls = ['http://sc.leju.com/', ]
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
        """提取楼盘封面等基本信息
        :param response: http response
        :return: request if house has detail_url else None
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
        detail_url = response.urljoin(
            response.xpath(u"//ul[@class='z_main_menu']//a[contains(text(),'楼盘详情')]/@href").extract_first())
        if detail_url:
            yield scrapy.Request(detail_url, meta={'house': house}, callback=self.parse_house_detail)
        else:
            self.logger.info(u'此楼盘详情信息: %s', house['url'])

    def parse_house_detail(self, response):
        """获取楼盘详情
        :param response: http response
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
        # house['lon_lat'] = ','.join([response.xpath('//script').re_first(".*?coordx='(\d+.\d+)'"), response.xpath(
        #     '//script').re_first(".*?coordy='(\d+.\d+)'.*")])
        house['developer'] = response.xpath(
            ur"//ul[@class='z_info_list clearfix']//li[contains(label,'\u5f00\u2002\u53d1\u2002\u5546\uff1a')]/p/text()").extract_first(
            u'未知').strip()
        house['property_company'] = response.xpath(
            u"//ul[@class='z_info_list clearfix']//li[contains(label, '物业公司')]/p/text()").extract_first(u'未知').strip()
        house['property_fee'] = response.xpath(
            u"//ul[@class='z_info_list z_info_list01 clearfix']//li[contains(label,'\u7269\u2002\u4e1a\u2002\u8d39\uff1a')]/text()").extract_first(
            u'未知').strip()
        house['decoration'] = response.xpath(
            u"//ul[@class='z_info_list clearfix']//li[contains(label, '装修情况')]/text()").extract_first(u'未知').strip()
        house['description'] = response.xpath("//div[@class='z_project_info']").extract_first(u'暂无').strip()
        # 楼盘户型图首页
        huxing_url = response.xpath(u"//ul[@class='z_main_menu']//a[contains(text(),'户型图')]/@href").extract_first()
        if huxing_url:
            self.logger.debug(u'楼盘图片首页: %s', huxing_url)
            house['layout_items'] = []
            yield scrapy.Request(url=response.urljoin(huxing_url), meta={'house': house}, callback=self.parse_houselayout)
        else:
            self.logger.info(u'此楼盘无户型图片: %s', house['url'])
            yield house

    def parse_houselayout(self, response):
        """
        func:户型信息处理
        """
        house = response.meta['house']
        huxing_records = response.xpath("//ul[@class='b_list01 clearfix']//li")
        for huxing_record in huxing_records:
            houselayout = SinaHouseLayout()
            houselayout['name'] = huxing_record.xpath(".//h2/span/text()").extract_first('未知').strip()
            img_url_tmp = huxing_record.xpath(".//img/@lsrc").extract_first()
            # 小图: http://src.leju.com/imp/imp/deal/a6/39/c/9bf2cb7d253475993fbce5a4c65_p7_mk7_cm358X269_wm47_pt1.jpg
            # 转换为大图的链接: http://src.leju.com/imp/imp/deal/a6/39/c/9bf2cb7d253475993fbce5a4c65_p7_mk7_wm47_pt1.jpg
            houselayout['img_url'] = img_url_tmp[:(img_url_tmp.index('mk7') + 3)] + "_wm47_pt1.jpg"
            houselayout['img_path'] = None
            houselayout['area'] = huxing_record.xpath(".//h3[1]/text()").extract_first()
            houselayout['price'] = huxing_record.xpath(
                "concat(.//h3[2]/text()[1],.//h3[2]/text()[2])").extract_first().strip()
            # 户型收集起来
            house['layout_items'].append(dict(houselayout))

        # 部分户型图有分页, 如: http://data.house.sina.com.cn/sc127009/huxing/#wt_source=data6_tpdh_hxt
        # 网站改版后新链接: http://house.leju.com/sc127009/huxing/
        next_url = response.xpath(u"//a[@class='next']/@href").extract_first()
        if next_url:
            self.logger.debug(u'进入楼盘户型图下一页: %s', next_url)
            yield scrapy.Request(url=response.urljoin(next_url), meta={'house': house,}, callback=self.parse_houselayout)
        else:
            self.logger.info(u'此楼盘链接处理完毕: %s', house['url'])
            yield house
