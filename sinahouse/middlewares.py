import random

class UserAgentMiddleware(object):   
    """add a random useragent to request"""  
      
    def __init__(self, agents):
        self.agents = agents
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    """add a random proxy to request"""
    
    def __init__(self, proxies):
        self.proxies =  proxies
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('PROXIES'))
    
    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)
        print request.meta
        
        
