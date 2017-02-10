### 简介
1. SinaHouseCrawler/house 基于scrapy, scrapy-redis实现的一个分布式网络爬虫,爬取了 ~~[新浪房产](http://data.house.sina.com.cn/sc/search/)~~ <sup id="a1">[1](#f1)</sup>**[乐居房产](http://sc.leju.com/)** 的楼盘信息及户型图片,实现了数据提取,去重,保存,分页数据的采集,数据的增量爬取,代理的使用,失效代理的清除,useragent的切换,图片的下载等功能,并且common模块中的中间件等可以在其他爬虫中复用.
2. SinaHouseCrawler/proxy 爬取了[西刺](http://www.xicidaili.com/nn/) 和[快代理](http://www.kuaidaili.com/)两个网站上的高匿名代理,通过代理访问[网易](http://www.163.com/)作为检验,保留访问成功的代理数据.

---
### 数据展示

**房产数据**
![房产数据](https://raw.githubusercontent.com/Fighting-Toghter/Exercise/master/images/house.png)
---
**户型数据**
![户型数据](https://raw.githubusercontent.com/Fighting-Toghter/Exercise/master/images/hosuelayout.png)
---
**CustomImagesPipeline下载的图片**
![图片](https://raw.githubusercontent.com/Fighting-Toghter/Exercise/master/images/image_store.png)
---
**ThreadImagesPipeline下载的图片**
![图片](https://raw.githubusercontent.com/Fighting-Toghter/Exercise/master/images/images.png)
---
** xici和kuaidaili的代理ip数据**
![图片](https://raw.githubusercontent.com/Fighting-Toghter/Exercise/master/images/proxyip.png)
---
### 功能清单:

1. 'sinahouse.pipelines.MongoPipeline'实现数据持久化到mongodb,'sinahouse.pipelines.MySQLPipeline'实现数据异步写入mysql

2. 'common.middlewares.UserAgentMiddleware','common.middlewares.ProxyMiddleware' 分别实现用户代理UserAgent变换和IP代理变换

3. 'sinahouse.pipelines.ThreadImagesPipeline','sinahouse.pipelines.CustomImagesPipeline'分别是基于多线程将图片下载保存到images文件夹和继承scrapy自带  ImagePipline的实现的图片下载保存到images_store

4. 'scrapy.extensions.statsmailer.StatsMailer'是通过设置settings中的mai等相关参数实现发送爬虫运行状态信息到指定邮件.scrapy.mail中的  MailSender也可以实现发送自定义内容邮件 

5. 通过设置setting中的scrapy-redis的相关参数,实现爬虫的分布式运行,或者单机多进程运行.无redis环境时,可以注释掉相关参数,转化为普通的scrapy爬虫程序  
6. 运行日志保存

---
### 运行环境:
1. 只在Python 2.7测试过,请先安装 requirements.txt 中的模块.
2. MySQLPipeline 用到的表:
```
CREATE TABLE `house` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `open_date` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `lon_lat` varchar(50) DEFAULT NULL,
  `developer` varchar(50) DEFAULT NULL,
  `property_company` varchar(50) DEFAULT NULL,
  `property_manage_fee` varchar(50) DEFAULT NULL,
  `decoration` varchar(50) DEFAULT NULL,
  `cover_path` varchar(128) DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  `url` varchar(128) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)

CREATE TABLE `house_layout` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `area` varchar(20) DEFAULT NULL,
  `img_path` varchar(128) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id_refs_id` (`house_id`)
)
```
---
### 其他说明
LOG_FORMATTER = 'sinahouse.utils.PoliteLogFormatter', 实现raise DropItem()时避免scrapy弹出大量提示信息; 图片保存路径,数据库连接等参数,请根据自己环境设置; 更多相关信息请查阅scrapy以及scrapy-redis文档  
  
---  
### 测试方法： 
方法一:
```
scrapy crawl leju -s CLOSESPIDER_ITEMCOUNT=3 -o newhouse.json
```
查看newhouse.json中的数据是否与house.json中的数据类似.
方法二:
```
scrapy parse --spider=leju  -c parse_house -d 9 "http://house.leju.com/sc129079/#wt_source=pc_search_lpxx_bt"
```
查看item是否提取成功,windows cmd下显示可能为乱码.

数据中各个字段的**意义**，请查看 **house.items**以及**common.items.house** 中的注释。 
---
### 运行方法:  
---
一. sinahouse运行
####单机:
```
  cd SinaHouseCrawler/house/    
  scrapy crawl leju 
```
####分布式:    
 配置好setting中的scrapy-redis的相关参数,在各机器中分别按单机方式启动即可    
  
**爬取目标网站**: [新浪房产](http://data.house.sina.com.cn/sc/search/)

---
二. xici和kuaidaili运行
```
  cd SinaHouseCrawler/proxy/
  scrapy crawl xici -o xici.json
  scrapy crawl kuaidaili -o kuaidaili.json
 ```
 **爬取目标网站**: [西刺](http://www.xicidaili.com/nn/) 和[快代理](http://www.kuaidaili.com/)
 
---

<b id="f1">1</b> 网站大改版,原是[新浪房产](http://data.house.sina.com.cn/sc/search/),现改为[乐居房产](http://sc.leju.com/),链接由http://data.house.sina.com.cn 改为 http://sc.leju.com ,原始链接会跳转到新链接 [↩](#a1)
