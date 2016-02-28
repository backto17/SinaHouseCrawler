# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SinaHouseItem(scrapy.Item):
    save_path = scrapy.Field()
    source_id = scrapy.Field()
    index_url = scrapy.Field()
    community_id = scrapy.Field()
    community_name = scrapy.Field()
    city_id = scrapy.Field() 
    city_name = scrapy.Field()   
    area_id = scrapy.Field()
    area_name = scrapy.Field() 
    address = scrapy.Field() 
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    developer = scrapy.Field() 
    community_desc = scrapy.Field()
    property_manage_fee = scrapy.Field() 
    property_manage_com = scrapy.Field() 
    bus = scrapy.Field() 
    metro = scrapy.Field() 
    cover_id = scrapy.Field()   
    open_date = scrapy.Field()  
    check_in_date = scrapy.Field()
    house_img_urls = scrapy.Field()
    cover_url = scrapy.Field()   
    household_size = scrapy.Field()
    per_square_price = scrapy.Field()
    decoration = scrapy.Field()
    property_type = scrapy.Field()
    construction_area = scrapy.Field()
    image_paths = scrapy.Field()
    
    
