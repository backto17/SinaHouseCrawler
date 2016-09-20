# coding: utf-8
'''
@date: 2016-09-20
@author: alex.lin
'''
from scrapy.exceptions import DropItem

class RemoveDuplicatePipeline(object):
    """class: 根据指定的key,去除重复的item"""
    
    records = set()
    def __init__(self, key='source_id'):
        self.key = key
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DISTINCT_KEY', 'source_id'))
        
    def process_item(self, item, spider):
        if item[self.key] not in self.records:
            return item
        else:
            raise DropItem('Duplicate %s: %s' %(self.key, item[self.key]))
    
