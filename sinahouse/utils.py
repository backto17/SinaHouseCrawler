# coding: utf-8
# author: alex lin
import threading
import logging
from scrapy import logformatter

class semaphore_thread(threading.Thread):
    semaphore = threading.Semaphore(32)
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


