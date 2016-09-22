# coding: utf-8
'''
@date: 2016-09-08

@author: LG
'''
import abc
import logging

from twisted.enterprise import adbapi

class AsyncSqlPipelineBase(object):
    """
    class:异步写入关系型数据库的基础管道,继承的子类必须完成 process_item方法.
    支持DB-API 2.0 compliant database
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, database_info, stats):
        """
        para: stats , crewler 的stats
        database_info 应该包含对应数据库的连接信息
        egg：database_info = {
            'dbapiName': 'MySQLdb',
            'host' : '192.168.3.238',
            'db' : 'test',
            'user' : 'alex',
            'passwd' : 'alex',
#             'cursorclass' : MySQLdb.cursors.DictCursor,
            'charset' : 'utf8',
            'use_unicode' : True
            }
        """
        self.dbpool = adbapi.ConnectionPool(**database_info)
        self.stats = stats
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        """
        func:从当前爬虫配置文件获取数据库连接所需信息
        """
        database_info = crawler.settings.get('DATABASE_INFO')
        stats = crawler.stats
        return cls(database_info, stats)
    
    @abc.abstractmethod
    def process_item(self,item, spider):
        """
        func: process items as you wish
        """
        pass
    
    def close_spider(self,spider):
        """
        func: 关闭数据库连接
        """
        self.dbpool.close()
        
    