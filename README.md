#SinaHouseCrawler
##基于scrapy,scrapy-redis实现的一个分布式网络爬虫,爬取了新浪房产的楼盘信息及户型图片,实现了常用的爬虫功能需求.
1.'sinahouse.pipelines.MongoPipeline' 实现数据持久化到mongodb  
2.'sinahouse.middlewares.UserAgentMiddleware','sinahouse.middlewares.ProxyMiddleware' 分别实现用户代理UserAgent变换和IP代理变换  
3.'sinahouse.pipelines.ImagePipeline','sinahouse.pipelines.CustomImagesPipeline'分别是基于多线程的图片下载保存和继承scrapy自带  ImagePipline的实现的图片下载保存  
4.'scrapy.extensions.statsmailer.StatsMailer'是通过设置settings中的mai等相关参数实现发送爬虫运行状态信息到指定邮件.scrapy.mail中的  MailSender也可以实现发送自定义内容邮件  
5.通过设置setting中的scrapy-redis的相关参数,实现爬虫的分布式运行,或者单机多进程运行.无redis环境时,可以注释掉相关参数,转化为普通的  scrapy爬虫程序  
6.运行日志保存

其他说明.LOG_FORMATTER = 'sinahouse.utils.PoliteLogFormatter', 实现raise DropItem()时避免scrapy弹出大量提示信息; 图片保存路径,数据库连接等参数,请根据自己环境设置; 更多相关信息请查阅scrapy以及scrapy-redis文档
  运行前,请先安装 requirements.txt 中的模块! 
  运行方法:
  单机: 
  cd SinaHouseCrawler
  scrapy crawl sinahouse
 分布式:
 配置好setting中的scrapy-redis的相关参数,在各机器中分别按单机方式启动即可
  爬取目标网站:[新浪房产](http://data.house.sina.com.cn/sc/search/)  
