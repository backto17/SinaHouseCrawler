# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from common.items.house import HouseItemBase, HouseLayoutItemBase

class SinaHouseLayout(HouseLayoutItemBase):
    price = scrapy.Field() # 此户型价格

class SinaHouseItem(HouseItemBase):
    source_id = scrapy.Field() # 楼盘在新浪房产的id
    description = scrapy.Field() # 楼盘简介
    

    
    
