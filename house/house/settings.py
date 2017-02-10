# -*- coding: utf-8 -*-

import os
import sys
import datetime

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, PROJECT_ROOT)

BOT_NAME = 'house'
SPIDER_MODULES = ['house.spiders']
NEWSPIDER_MODULE = 'house.spiders'
DOWNLOAD_HANDLERS = {'s3': None,}
FEED_EXPORT_ENCODING = 'utf-8'
# AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED=False
CONCURRENT_ITEMS = 10
CONCURRENT_REQUESTS = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 10

DEPTH_LIMIT = 0
DOWNLOAD_TIMEOUT = 20
DOWNLOAD_DELAY = 0.5

HTTPCACHE_ENABLED = False

REDIRECT_ENABLED = False
RETRY_ENABLED = True
REACTOR_THREADPOOL_MAXSIZE = 30

# LOG_FORMATTER = 'house.utils.PoliteLogFormatter'


IMAGE_PATH = os.path.join(os.path.abspath('.'),'images')
IMAGES_STORE = os.path.join(os.path.abspath('.'),'images_store')

# LOG_ENABLED = False
# LOG_FILE = '%s%s%s' % ('sinahouse_',datetime.datetime.now().strftime('%Y%m%d%H%M%S'),'.log')
LOG_LEVEL = 'DEBUG'

# MONGO_HOST = "localhost"
# MONGO_PORT = 27017
# MONGO_DATABASE = "house"
# MONGO_COLLECTION = 'sina_item'

#################################################  settings for mysql  #################################################
DATABASE_INFO = {
            'dbapiName': 'MySQLdb',
            'host' : '192.168.3.170',
            'db' : 'sina',
            'user' : 'sina',
            'passwd' : '123456',
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


DOWNLOADER_MIDDLEWARES = {
    'common.middlewares.useragent.UserAgentMiddleware': 730,
    # 'common.middlewares.proxy.ProxyMiddleware': 735,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 740,
}

EXTENSIONS = {
            'scrapy.telnet.TelnetConsole': 200,
#             'scrapy.extensions.statsmailer.StatsMailer': 500,
}


ITEM_PIPELINES = {
                  'common.pipelines.RemoveDuplicatePipeline': 50,
#                 'house.pipelines.SinaHouseRemoveDuplicatePipeline' : 100,
#                   'house.pipelines.ThreadImagesPipeline': 200,
#                   'house.pipelines.CustomImagesPipeline': 300,
#                   'house.pipelines.MongoPipeline':400,
#                 'house.pipelines.MySQLPipeline': 500,
                
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
{"http": "118.169.112.211:8080"},
{"http": "110.73.12.61:8123"},
{"http": "61.227.228.121:8080"}
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