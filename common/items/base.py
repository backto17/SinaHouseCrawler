# coding: utf-8
'''
@date: 2016-09-08
@author: alex.lin
'''
from scrapy.item import Item, Field

class BaseItem(Item):
    """
    基础item, 包含通用属性
    """
    url = Field() # 来源url
    project = Field() # 项目名字
    spider = Field() # 爬虫名字
    server = Field() # 服务器
    create_time = Field() # 爬取时间