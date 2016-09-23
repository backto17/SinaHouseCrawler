# coding: utf-8
'''
@date: 2016-09-22
@author: alex.lin
'''

import random
import logging

logger = logging.getLogger(__name__)

class UserAgentMiddleware(object):   
    """add a random useragent to request"""  
      
    def __init__(self, agents):
        self.agents = agents
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.agents)