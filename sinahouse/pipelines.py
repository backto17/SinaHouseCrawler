# -*- coding: utf-8 -*-
'''
modified on 2016-05-17

@author: alex
'''
import threading
import logging
import md5

import pymongo
import scrapy  
from scrapy.mail import MailSender 
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import requests
from common.pipelines import AsyncSqlPipelineBase

from utils import semaphore_thread

logging.getLogger("requests").setLevel(logging.WARNING)

class MongoPipeline(object):
    """
    Mongo存储管道
    """
    def __init__(self, settings):
        self.settings = settings
        self.client = pymongo.MongoClient(host=settings.get('MONGO_HOST'), port=settings.get('MONGO_PORT'))
        self.db = self.client[settings.get('MONGO_DATABASE')]
        self.collection = settings.get('MONGO_COLLECTION')
                
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)
    
    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
#         mailer = MailSender.from_settings(self.settings)        
#         mailer.send(to=["lingang@xxx.com"], subject="THANKS", body="THANKS YOU!",cc=[])

class MySQLPipeline(AsyncSqlPipelineBase):
    '''
    func:数据写入 mysql的管道
    '''
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert, item)
        query.addErrback(self._handle_error)
        return item
    
    def _insert(self, cursor, item):
        """
        func: 插入数据库,
        house_info信息如下:
        CREATE TABLE `house_info` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `house_name` varchar(300) DEFAULT NULL,
          `house_index_url` varchar(300) DEFAULT NULL,
          `house_price` varchar(100) DEFAULT NULL,
          `house_address` varchar(500) DEFAULT NULL,
          `longtitude_latitude` varchar(100) DEFAULT NULL,
          `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`)
        )
        """
        cursor.execute(""" 
        insert into  house_info(house_name,house_index_url,house_price,house_address,longtitude_latitude)
        values (%s,%s,%s,%s,%s)""",(item['community_name'],item['index_url'],item['per_square_price'],item['address'],item['longtitude_latitude']))
        
        self.stats.inc_value('mysql_items_added', count=1, start=0)
             
    def _handle_error(self,e):
        self.stats.inc_value('mysql_items_failed', count=1, start=0)
        self.logger.error(e)

        
class ThreadImagesPipeline(object):
    """
    func:利用 threading,requests 下载图片;
    semaphore_thread 封装了信号量,控制下载线程数
    """
    def __init__(self,image_path):
        self.image_path = image_path
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings.get('IMAGE_PATH'))
    
    def process_item(self, item, spider):
        semaphore_thread(target=self.process_imgage, args=(item,)).start()
        return item
    
    def process_imgage(self,item):
        item['cover_info']['file_path'] = self.save_image(item['cover_info']['url'])
        for houselayout in item['layout_items']:
            houselayout['img_info']['file_path'] = self.save_image(houselayout['img_info']['url'])
            
    def save_image(self,url, retry=2):
        while retry:
            try:
                resp = requests.get(url,timeout=(10,60))
                break
            except requests.exceptions.Timeout:
                if retry:
                    retry -= 1
                    continue
                logging.error('requests.exceptions.Timeout: image saving failed in %s',url)
                return 
            except Exception as e:
                if retry:
                    retry -= 1
                    continue
                logging.error('Download Failed: image saving failed in %s, Exception: %s', url, e)
                return
            
        file_path = '%s%s.jpg' % (self.image_path, md5.md5(url).hexdigest())
        with open(file_path, 'wb') as f:
            f.write(resp.content)
            return file_path
    
    def close_spider(self,spider):
        for t in threading.enumerate():
            if isinstance(t,semaphore_thread):
                t.join()
    
            
class CustomImagesPipeline(ImagesPipeline):
    """
    func:继承scrapy自带ImagesPipeline,
    实现自己的功能需求
    """
    def get_media_requests(self, item, info):
        if item['cover_info']['url']:
            yield scrapy.Request(item['cover_info']['url'])
        for layout in item['layout_items']:
            yield scrapy.Request(layout['img_info']['url'])
            
    def item_completed(self, results, item, info):
        if item['cover_info']['url']:
            item['cover_info']['path'] = results[0][1]['path'] if results[0][0] else ''
            results = results[1:]
        for i,(ok, result) in enumerate(results):
            item['layout_items'][i]['img_info']['path'] = result['path'] if ok else ''
        return item