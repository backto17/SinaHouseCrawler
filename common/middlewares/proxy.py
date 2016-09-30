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
        self.proxies = {'http': set(),
                        'https':set(),}
        for proxy in proxies:
            self.proxies['http'].add(proxy.get('http'))
            self.proxies['https'].add(proxy.get('https'))
            
        self.proxies['http'].discard(None)
        self.proxies['https'].discard(None)
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXIES'))
    
    def process_request(self, request, spider):
        scheme = self.get_scheme(request.url)
        keep_proxy = request.meta.get('keep_proxy', False)
        retries = request.meta.get('retry_times', 0)
        if 'proxy' in request.meta:
            if keep_proxy:
                return
            elif retries == 2:
                    logger.warning('Bad %s proxy: %s', scheme, request.meta['proxy'])
                    self.remove_bad_proxy(scheme, request.meta['proxy'])
        proxy = self.get_proxy(scheme)
        if proxy:
            request.meta['proxy'] = proxy
                
    @staticmethod
    def get_scheme(url):
        if url.startswith('http:'):
            return 'http'
        else:
            return 'https'
    
    def remove_bad_proxy(self, scheme, proxy):
        proxy = proxy[proxy.rindex('/')+1:]
        self.proxies[scheme].discard(proxy)
    
    def get_proxy(self,scheme):
        if self.proxies[scheme]:
            return '%s://%s' %(scheme, random.sample(self.proxies[scheme],1)[0])