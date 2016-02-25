# -*- coding: utf-8 -*-


# from scrapy.exceptions import DropItem
# import utils
# import MySQLdb 
import pymongo  
from scrapy.mail import MailSender 

class MongoPipeline(object):
    collection_name = "scrapy_items"
    def __init__(self, mongo_uri=("localhost",27017), mongo_db="sinahouse",settings=None):
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
        mailer = MailSender.from_settings(self.settings)
        self.client.close()
#         mailer.send(to=["lingang_upc@163.com"], subject="Some subject", body="Some body",cc=[])
        
#     def close_spider(self,spider):
#         for t in threading.enumerate():
#             if isinstance(t,semaphore_thread):
#                 t.join()
    
            
