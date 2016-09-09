# coding: utf-8
'''
@date: 2016-09-09
@author: alex.lin
'''
import scrapy

from .baseitem import BaseItem


class HouseItemBase(BaseItem):
    """
    class: 房产类的基础Item
    """
    name = scrapy.Field() # 楼盘名称
    open_date = scrapy.Field() # 开盘时间
    check_in_date = scrapy.Field() # 入住时间
    address = scrapy.Field() # 地址(北京某某区某某路...)
    longtitude_latitude = scrapy.Field() # 经度 纬度
    developer = scrapy.Field() # 开发商
    property_manage_fee = scrapy.Field() # 物业费
    property_manage_com = scrapy.Field() # 物业公司
    price = scrapy.Field() # 价格
    decoration = scrapy.Field() # 装修情况
    cover_url = scrapy.Field() # 楼盘封面图片
    layout_items = scrapy.Field() # 户型信息
    
class HouseLayoutItemBase(BaseItem):
    """
    class: 楼盘户型的基础item
    """
    name = scrapy.Field() # 户型名称
    area = scrapy.Field() # 户型面积
    img_url = scrapy.Field() # 户型图片
    