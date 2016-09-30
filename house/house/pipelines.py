# -*- coding: utf-8 -*-
'''
modified on 2016-05-17

@author: alex
'''
import threading
import logging
import md5
import os 

import pymongo
import scrapy  
from scrapy.mail import MailSender 
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import requests
import MySQLdb

from common.pipelines import AsyncSqlPipelineBase, RemoveDuplicatePipeline
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
        """
        cursor.execute(""" 
        insert into  house(
        name, price, open_date, address, lon_lat, developer, property_company,
         property_manage_fee, decoration, cover_path, source_id, url,create_time)
        values (%(name)s, %(price)s, %(open_date)s, %(address)s, %(lon_lat)s ,%(developer)s ,%(property_company)s ,%(property_manage_fee)s ,%(decoration)s  ,%(cover_path)s ,%(source_id)s ,%(url)s ,%(create_time)s
        )""", dict(item))
        house_id = cursor.lastrowid 
        self.logger.info('source_id:%s, name: %s, id: %s',item['source_id'],item['name'],house_id)
        self.stats.inc_value('mysql_items_added', count=1, start=0)
        for houselayout in item['layout_items']:
            houselayout['house_id'] = house_id
            cursor.execute("""
            insert into house_layout(house_id, name, area, img_path, price)
            values (%(house_id)s, %(name)s, %(area)s, %(img_path)s, %(price)s)
            """, houselayout)
            
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
        try:
            os.mkdir(self.image_path)
        except:
            pass

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings.get('IMAGE_PATH'))
    
    def process_item(self, item, spider):
        semaphore_thread(target=self.process_imgage, args=(item,)).start()
        return item
    
    def process_imgage(self,item):
        item['cover_path'] = self.save_image(item['cover_url'])
        for houselayout in item['layout_items']:
            houselayout['img_path'] = self.save_image(houselayout['img_url'])
            
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
   
        file_path = '%s%s%s.jpg' % (self.image_path, os.path.sep, md5.md5(url).hexdigest())
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
        if item['cover_url']:
            yield scrapy.Request(item['cover_url'])
        for layout in item['layout_items']:
            yield scrapy.Request(layout['img_url'])
            
    def item_completed(self, results, item, info):
        if item['cover_url']:
            item['cover_path'] = results[0][1]['path'] if results[0][0] else None
            results = results[1:]
        for i,(ok, result) in enumerate(results):
            item['layout_items'][i]['img_path'] = result['path'] if ok else None
        return item

class SinaHouseRemoveDuplicatePipeline(RemoveDuplicatePipeline):
    """
    class: 新浪房产的去重pipeline
    """
    def open_spider(self, spider):
        database_info = spider.settings.get('DATABASE_INFO')
        database_info.pop('dbapiName')
        connection = MySQLdb.connect(**database_info)
        cursor = connection.cursor()
        cursor.execute('select distinct source_id from house')
        source_ids = cursor.fetchall()
        for (source_id,) in source_ids:
            self.records.add(source_id)
        
