# -*- coding: utf-8 -*-
'''
modified on 2016-05-17

@author: alex
'''
import threading
import logging

from twisted.enterprise import adbapi
import pymongo
import scrapy  
from scrapy.mail import MailSender 
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import requests

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

class MySQLPipeline(object):
    '''
    数据写入 mysql的管道
    '''
    def __init__(self, stats, mysql_info):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **mysql_info)
        self.stats = stats
        self.logger = logging.getLogger(__name__)
        
    @classmethod
    def from_crawler(cls, crawler):
        '''
        获取数据库连接信息
        '''
        mysql_info = crawler.settings.get('MYSQL_INFO')
        stats = crawler.stats
        return cls(stats, mysql_info)
        
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert, item)
        query.addErrback(self._handle_error)
        return item
    
    def _insert(self, tx, item):
        tx.execute(""" 
        insert into  house_info(house_name,house_index_url,house_price,house_address,longtitude_latitude)
        values (%s,%s,%s,%s,%s)""",(item['house_name'],item['house_index_url'],item['house_price'],item['house_address'],item['longtitude_latitude']))
        
        self.stats.inc_value('mysql_items_added', count=1, start=0)
             
    def _handle_error(self,e):
        self.stats.inc_value('mysql_items_failed', count=1, start=0)
        self.logger.error(e)
    
    def close_spider(self,spider):
        self.dbpool.close()
        
class ImagePipeline(object):
    """
    利用 threading,requests 下载图片;
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
        self.save_image(*item['cover_url'])
        for house_img in item['house_img_urls']:
            self.save_image(house_img[3],house_img[0])
            
    def save_image(self,url,img_id):
        try:
            resp = requests.get(url,timeout=(10,60))
        except requests.exceptions.Timeout:
            logging.debug('requests.exceptions.Timeout: image saving failed in %s',url)
            return
        except Exception:
            logging.debug('Download Timeout: image saving failed in %s',url)
            return
            
        image = self.image_path + img_id + '.jpg'
        with open(image, 'wb') as f:
            f.write(resp.content)
    
    def close_spider(self,spider):
        for t in threading.enumerate():
            if isinstance(t,semaphore_thread):
                t.join()
    
            
class CustomImagesPipeline(ImagesPipeline):
    """
    继承scrapy自带ImagesPipeline,
    实现自己的功能需求
    """
    def get_media_requests(self, item, info):
        for image_id,huxing,size,image_url in item['house_img_urls']:
            yield scrapy.Request(image_url)
            
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item