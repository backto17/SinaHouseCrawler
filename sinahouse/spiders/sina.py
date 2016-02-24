#coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sinahouse.items import HouseItem
import re
import time
# from scrapy.selector import Selector
import sys
sys.path.append('E:\code\java\spider')
reload(sys)
from standardization.standarlize import judge_type,pretty_json
from sinahouse import settings


class SinaSpider(CrawlSpider):
    name = 'sina'
    allowed_domains = ['house.sina.com.cn']
    start_urls = ['http://data.house.sina.com.cn/sc/search/?keyword=&charset=utf8',]
    rules = [
            Rule(LinkExtractor(allow = ('/\w+\d+?.*bt\d*')),callback='parse_item',follow=False),
            Rule(LinkExtractor(allow = ('^http://data.house.sina.com.cn/\w+/search/$')),process_links="parse_city_links"), #各个城市链接提取
#              Rule(LinkExtractor(allow = ('^http://data.house.sina.com.cn/\w+/search-\d*/\?bcity=\w*$'))), #
            Rule(LinkExtractor(allow = ('/\w+/search-\d*/.*'))),
 
            ]
#     ,process_links="parse_city_next_links"
#     def parse_city_next_links(self,links):
#         for link in links:
#             link.url = "http://data.house.sina.com.cn" + link.url
#         return links
    def parse_city_links(self,links):
        for link in links:
            link.url = link.url +'?keyword=&charset=utf8'
        return links
        
    def parse_item(self,response):
        item = HouseItem()
        item['source_id'] = settings.SOURCE
        item['save_path'] = settings.IMAGE_PATH
        item['community_name'] = response.xpath('/html/body/div[1]/div[9]/div[1]/h2/text()').extract_first()
        item['index_url'] = response.url
#         item['kaipan_date'] = '-'.join(re.findall('(\d+)',response.xpath(u"//div[@class='info wm']//li[contains(span,'开盘时间')]/div/@title").extract_first()))
        item['open_date'] = '-'.join(re.findall('(\d+)',response.xpath(u"//*[@id='callmeBtn']/ul/li[4]/span[2]/text()").extract_first(default=u'待定').strip()))
        item['check_in_date'] = '-'.join(re.findall('(\d+)',response.xpath(u'(//*[@id="callmeBtn"]//div[@title])[2]/@title').extract_first(default=u'待定')))
        item['developer'] = response.xpath(u"//div[@class='info wm']/ul/li[3]/text()").extract_first(default=u'未知').strip()
        item['property_manage_com'] = response.xpath(u"//li[contains(span,'物业公司')]/text()").extract_first(default=u'未知').strip()
        item['address'] = response.xpath(u'//*[@id="callmeBtn"]/ul/li[2]/span[2]/text()').extract_first(default=u'未知').strip()
        item['area_name'] = response.xpath("//span[@class='fl']/a[3]//text()").extract_first(default=u'未知').strip()
        item['city_name'] = response.xpath("//span[@class='fl']/a[1]//text()").extract_first(default=u'未知').replace(u'房产','').strip()
        item['cover_urls'] = response.xpath("//*[@id='con_tab1_con_3']/a/img/@lsrc").extract_first()
        item['household_size'] = response.xpath("//div[@class='info wm']/ul/li[5]/text()").extract_first(default=u'未知').replace(u'户','').strip()
        item['property_manage_fee'] = response.xpath("//div[@class='info wm']/ul/li[7]/text()").extract_first(default=u'未知').strip()
        item['construction_area'] = response.xpath("//div[@class='info wm']/ul/li[9]/text()").extract_first(default=u'未知').strip()
        item['property_type'] = response.xpath("//div[@class='info wm']/ul/li[6]/text()").extract_first(default=u'未知').strip()
        item['decoration'] = response.xpath("//div[@class='info wm']/ul/li[12]/text()").extract_first(default=u'未知').strip()
        item['per_square_price'] = response.xpath("//*[@id='callmeBtn']/ul/li[1]/em[1]/text()").extract_first(default=u'未知').strip()

#         item['longitude'] = ''
#         item['latitude'] = ''
#         item['bus'] = ''
#         item['metro'] = ''
#         item['description'] = ''
        image_index_url = response.xpath('/html/body/div[1]/div[10]/ul/li[4]/a/@href').extract_first()
        
#         from scrapy.shell import inspect_response
#         inspect_response(response, self)
        if image_index_url:
            yield scrapy.Request(url=image_index_url, meta={"house_item": item}, callback=self.parse_item_image)
        else:
            self.logger.info(pretty_json((u'此楼盘无图片:' , item['community_name'] ,item['index_url'])))
    
    def parse_item_image(self,response):
        item = response.meta["house_item"]
        item['house_img_urls'] = []
        huxing_index_url = response.xpath(u"//div[@class='housingNav w']//li[contains(a,'户型图')]/a/@href").extract_first()
        if huxing_index_url:
            self.logger.debug(u'楼盘图片首页:' + huxing_index_url )
            yield scrapy.Request(url = huxing_index_url,meta={'house_item':item},callback=self.parse_item_huxing)
        else:
            self.logger.info(u'此楼盘无户型图片:' + item['community_name'] + item['index_url'])
            
    def parse_item_huxing(self,response):
        item = response.meta['house_item']
        lis = response.xpath("//div[@class='housingShow']//li")
        for li in lis:
            huxing = li.xpath(".//span[@class='infoSpan']/span/text()").extract_first(default=u'其他')
            img_src_url_tmp = li.xpath('.//img/@src').extract_first()
            img_src_url = img_src_url_tmp[:(img_src_url_tmp.index('mk7')+3)]+'.jpg'
            size = li.xpath(".//span[@class='infoSpanNum']/span/em/text()").extract_first(default=0)
            huxing_type = judge_type(huxing[:4])
            item['house_img_urls'].append((huxing,img_src_url,size,huxing_type))
            
        
        next_url = response.xpath(u"//span[@class='pagebox_next' and contains(a,'下一页')]/a/@href").extract_first()
        if next_url:
            self.logger.debug(u'进入楼盘户型图下一页:' + next_url )
            yield scrapy.Request(url = next_url,meta={'house_item':item},callback=self.parse_item_huxing)
        else:
            item['house_img_urls'] = len(item['house_img_urls'])
            self.logger.info(pretty_json(dict(item)))

            yield item
    
    
