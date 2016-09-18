# -*- coding: utf-8 -*-

import datetime
import os

BOT_NAME = 'sinahouse'
SPIDER_MODULES = ['sinahouse.spiders']
NEWSPIDER_MODULE = 'sinahouse.spiders'
DOWNLOAD_HANDLERS = {'s3': None,}

# AUTOTHROTTLE_ENABLED = True

# LOG_FORMATTER = 'sinahouse.utils.PoliteLogFormatter'
SOURCE = 15


IMAGE_PATH = os.path.join(os.path.abspath('.'),'images')
IMAGES_STORE = os.path.join(os.path.abspath('.'),'images_store')

# LOG_FILE = 'SinaHouse_' + str(datetime.datetime.today()).replace(' ','_').replace('-','_').replace(':','_') +  '.log'
LOG_LEVEL = 'DEBUG'

# MONGO_HOST = "localhost"
# MONGO_PORT = 27017
# MONGO_DATABASE = "sinahouse"
# MONGO_COLLECTION = 'custom_item'

#################################################  settings for mysql  #################################################
DATABASE_INFO = {
            'host' : '192.168.3.238',
            'db' : 'test',
            'user' : 'alex',
            'passwd' : 'alex',
#             'cursorclass' : MySQLdb.cursors.DictCursor,
            'charset' : 'utf8',
            'use_unicode' : True
            }


#################################################  settings for mailsender  #################################################

MAIL_FROM = 'ALEX.LIN@xxx.com'
MAIL_HOST = 'smtp.xxx.com'
MAIL_PORT = 25
MAIL_PASS = 'password'
MAIL_USER = 'ALEX.LIN@xxx.com'
STATSMAILER_RCPTS = ['ALEX.LIN@xxx.com',]

##############################################################################################################################

CONCURRENT_ITEMS = 10
REACTOR_THREADPOOL_MAXSIZE = 10
HTTPCACHE_ENABLED = False
CONCURRENT_REQUESTS = 10
# Disable cookies (enabled by default)
COOKIES_ENABLED=False
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOADER_MIDDLEWARES = {
#     'sinahouse.middlewares.UserAgentMiddleware': 730,
#     'sinahouse.middlewares.ProxyMiddleware': 735,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 740,
}

EXTENSIONS = {
            'scrapy.telnet.TelnetConsole': 200,
#             'scrapy.extensions.statsmailer.StatsMailer': 500,
}


ITEM_PIPELINES = {
#                 'sinahouse.pipelines.MongoPipeline':100,
#                 'sinahouse.pipelines.ThreadImagesPipeline':200,
#                 'sinahouse.pipelines.CustomImagesPipeline': 20,
}




USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

PROXIES = [
'http://119.188.94.145:80',
'http://121.41.73.79:8088',
'http://183.184.194.113:8090',
'http://182.90.13.192:80',
'http://182.90.9.47:80',
'http://182.90.13.151:80',
'http://182.90.27.165:80',
'http://182.90.26.172:80',
'http://183.141.75.201:3128',
'http://182.90.15.148:80',
'http://123.149.237.158:8090',
'http://182.90.40.105:80',
'http://211.144.76.58:9000',
'http://182.89.6.236:8123',
'http://121.31.48.154:8123',
'http://182.90.24.175:80'
]

#################################################  settings for scrapy-redis  #################################################

# Max idle time to prevent the spider from being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at the first time (because the queue is empty).
# SCHEDULER_IDLE_BEFORE_CLOSE = 10
  
#Enables scheduling storing requests queue in redis.
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
    
# Don't cleanup redis queues, allows to pause/resume crawls.
# SCHEDULER_PERSIST = False
    
# Schedule requests using a priority queue. (default)
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
    
# REDIS_HOST = '192.168.3.225'
# REDIS_PORT = 6379

################################################################################################################################
try:
    from settings_local import *
except:
    pass