# coding: utf-8
'''
@date: 2016-09-22
@author: alex.lin
'''

import random
import logging

logger = logging.getLogger(__name__)



class ProxyMiddleware(object):
    """add a random proxy to request"""
    
    def __init__(self, proxies):
        self.proxies = set(proxies)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXIES'))
    
    def process_request(self, request, spider):
        if 'proxy' in request.meta and request.meta['proxy'] in self.proxies:
            logger.warning('Bad proxy: %s', request.meta['proxy'])
            self.proxies.remove(request.meta['proxy'])
        if self.proxies:
            request.meta['proxy'] = random.sample(self.proxies,1)[0]