# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SinaHouseItem(scrapy.Item):
    save_path = scrapy.Field() # 保存路径
    source_id = scrapy.Field() # 来源
    index_url = scrapy.Field() # 楼盘首页
    community_id = scrapy.Field() # 楼盘id
    community_name = scrapy.Field() # 楼盘名称
    city_id = scrapy.Field() # 城市
    city_name = scrapy.Field() # 城市名(北京,上海...)
    area_id = scrapy.Field() # 区域id
    area_name = scrapy.Field() # 区域名称(某某区,某某县...)
    address = scrapy.Field() # 地址(北京某某区某某路...)
    longitude = scrapy.Field() # 经度
    latitude = scrapy.Field() # 纬度
    developer = scrapy.Field() # 开发商
    community_desc = scrapy.Field() # 楼盘简介
    property_manage_fee = scrapy.Field() # 物业费
    property_manage_com = scrapy.Field() # 物业公司
    bus = scrapy.Field() # 公交路线
    metro = scrapy.Field() # 地铁路线
    cover_id = scrapy.Field() # 封面
    open_date = scrapy.Field() # 开盘时间
    check_in_date = scrapy.Field() # 入住时间
    house_img_urls = scrapy.Field()  # 户型链接,格式:[[
                                                    #         "1eda83d9a0684aab859d0c9edd97cbba",
                                                    #         "3室2厅2卫",
                                                    #         "117",
                                                    #         "http://src.house.sina.com.cn/imp/imp/deal/d0/bd/7/55e98457a56ef2ce06bf9d327a5_p7_mk7.jpg"
                                                    #       ], ]
    cover_url = scrapy.Field() # 封面链接  
    household_size = scrapy.Field() # 总户数：如小区总共住2000户
    per_square_price = scrapy.Field() # 每平米价格
    decoration = scrapy.Field() # 装修情况
    property_type = scrapy.Field() # 物业类型：普通住宅,公寓,写字楼,商铺,商住,建筑综合体...
    construction_area = scrapy.Field() # 建筑面积
    image_paths = scrapy.Field() # 使用scrapy, ImagesPipeline需要的字段
    
    
