# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from photohandler.save_img import save_huxing_img,save_picture
from database.dbutils import execute_select,POOL
from scrapy.exceptions import DropItem
import numpy
import logging
from standardization.standarlize import pretty_json
import threading
import MySQLdb
from scrapy import logformatter
import time
import re
import uuid
import traceback
import datetime
  
import pymongo  
from scrapy.mail import MailSender 

class MongoPipeline(object):
    collection_name = "scrapy_items"
    def __init__(self, mongo_uri=("localhost",27017), mongo_db="mail",settings=None):
        self.client = pymongo.MongoClient(*mongo_uri)
        self.db = self.client[mongo_db]
        self.settings = settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)
    
    def process_item(self,item,spider):
        self.db["item"].insert_one(dict(item))
        return item

    def close_spider(self,spider):
#         mailer = MailSender()
#         mailer = MailSender.from_settings(self.settings)
        
        self.client.close()
#         mailer.send(to=["lingang_upc@163.com"], subject="Some subject", body="Some body",cc=[])





























  
class HouseProjectPipeline(object):        
    def process_item(self, item, spider):
#         if self.item_satisfied(item):
#             logging.info(pretty_json(item.items()))
        thread = semaphore_thread(target=self.worker,args=(item,))
        thread.start()
            
        return item
           
    def item_satisfied(self,item):
        if not self.standardize_date_info(item):
            return False
        if item['kaipan_date']<'2013-01-01':
            return False
        if item['huxing_img_urls'] and item['name'] and item['kaipan_date'] and item['cover_urls']:
            sql = """SELECT
                    city_id,
                    city_name,
                    area_id,
                    area_name
                FROM
                    map_view
                WHERE
                    area_name LIKE '%%%s%%'
                AND (
                    city_name LIKE '%%%s%%'
                    OR province_name LIKE '%%%s%%') LIMIT 1 """%(item['area_name'].replace(u'县','').replace(u'区','').replace(u'市','').replace(u'旗','').replace(u'镇',''),item['city_name'],item['city_name'])
            try:
                item['city_id'],item['city_name'],item['area_id'],item['area_name'] = execute_select(sql)[0]
            except MySQLdb.OperationalError,e:
                logging.error(e)
                return False
            except Exception,e:
                logging.info(pretty_json((u'未查到区域信息',item['name'],item['city_name'],item['area_name'])))
                return False
        else:
            return False
        try:
            sql = 'SELECT id from community_view where community_name = "%s" and area_id=%s and city_id=%s LIMIT 1'%(item['name'],item['area_id'],item['city_id'])
            item['house_id'] = execute_select(sql)[0]
            if item['house_id']:
                logging.info(pretty_json((u'小区已存在',item['name'],item['kaipan_date'],item['index_url'])))
                return False
        except MySQLdb.OperationalError,e:
                logging.error(e)
                return False
        except Exception,e:
                logging.info(pretty_json((u'新增小区信息',item['index_url'],item['name'],item['city_name'],item['area_name'],item['kaipan_date'],item['ruzhu_date'])))
                        
        return True
    
    def save_cover_urls(self,item):
        back_id = str(uuid.uuid1()).replace('-','')
        item['no'] = back_id
        if not save_picture(item['cover_urls'], 'cover.jpg', 0,back_id,item['path']):
            return False
        
        #插入楼盘
        try:
            item['house_id'] = self.insert_house(item)
#             print u"楼盘 Id是:" ,house.id 
        except Exception,e:
            print u"插入楼盘失败",e
            traceback.print_exc()
            return False
        return True
    
    def insert_house(self,item):
        conn = POOL.connection()
        cur = conn.cursor()
        if item['ruzhu_date']==u'待定' or item['ruzhu_date'] ==None:
            sql = '''insert into 
            location_community(state,name,address,longitude,latitude,developer,pm_company,kaipan_date ,area_id,houselayout_count,no,create_time,modify_time,bus,metro,slug,head_slug)
                        values("%s", "%s",  "%s",    "%s",     "%s",    "%s",        "%s",     "%s",  "%s",        %s,         "%s",    "%s",    "%s",      "%s","%s","%s","%s") 
                        '''%(0,item['name'],item['address'],item['longitude'],item['latitude'],item['developer'],
                             item['pm_company'],item['kaipan_date'],item['area_id'],0,item['no'],datetime.datetime.today(),datetime.datetime.today(),item['bus'],item['metro'],' ',' ' )
#     print sql
        else:
            sql = '''insert into 
            location_community(state,name,address,longitude,latitude,developer,pm_company,kaipan_date,ruzhu_date,  area_id,houselayout_count,no,create_time,modify_time,bus,metro,slug,head_slug)
                        values("%s", "%s",  "%s",    "%s",     "%s",    "%s",        "%s",     "%s",      "%s",       "%s",    %s,          "%s",    "%s",    "%s"     ,"%s","%s"  ,"%s","%s") 
                        '''%(0,item['name'],item['address'],item['longitude'],item['latitude'],item['developer'],
                             item['pm_company'],item['kaipan_date'],item['ruzhu_date'],item['area_id'],0,item['no'],datetime.datetime.today(),datetime.datetime.today(),item['bus'],item['metro'],' ',' ' )
        
    #     print sql
        cur.execute(sql)
        house_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        return house_id
    
    def worker(self,item):
        if self.item_satisfied(item):
            if self.save_cover_urls(item):
                save_huxing_img(item['huxing_img_urls'],item['city_name'],item['house_id'],item['path'],item['source'])
        
    def close_spider(self,spider):
        for t in threading.enumerate():
            if isinstance(t,semaphore_thread):
                t.join()
    
    def standardize_date_info(self,item):
        try:
            if item['ruzhu_date'] == u'待定':
                pass
            else:
                if len(item['ruzhu_date'])==4:
                    item['ruzhu_date'] = item['ruzhu_date'] + '-01-01'
                elif len(item['ruzhu_date'])==7:
                    item['ruzhu_date'] = item['ruzhu_date'] + '-01'
                else:
                    item['ruzhu_date'] = item['ruzhu_date'][:10]
                
                if not re.match('\d{4}-\d{2}-\d{2}',item['ruzhu_date']):
                    item['ruzhu_date'] = u'待定'
                    
            if len(item['kaipan_date'])==4:
                item['kaipan_date'] = item['kaipan_date'] + '-01-01'
            elif len(item['kaipan_date'])==7:
                item['kaipan_date'] = item['kaipan_date'] + '-01'
            else:
                item['kaipan_date'] = item['kaipan_date'][:10]
                
            if not re.match('\d{4}-\d{2}-\d{2}',item['kaipan_date']):
                logging.info(pretty_json((u'开盘时间不对',item['kaipan_date'])))
                return False
        except:
            return False
        
        return True

            
class semaphore_thread(threading.Thread):
    semaphore = threading.Semaphore(16)
    def __init__(self,target=None,args=()):
        super(semaphore_thread, self).__init__()
        self.func = target
        self.args = args
    def run(self):
        with self.semaphore:
            self.func(*self.args)
    @classmethod
    def alter_max_semaphore(cls,num):
        if isinstance(num, int):
            semaphore_thread.semaphore = threading.Semaphore(num)
            
            


class PoliteLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.DEBUG,
            'msg': logformatter.DROPPEDMSG,
            'args': {
                'exception': exception,
                'item': item,
            }
        }