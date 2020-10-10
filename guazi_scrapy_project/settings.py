# Scrapy settings for guazi_scrapy_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# scrapybot
BOT_NAME = 'guazi_scrapy_project'

# 解析器的模块
SPIDER_MODULES = ['guazi_scrapy_project.spiders']
NEWSPIDER_MODULE = 'guazi_scrapy_project.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# 可以在settings中设置，也可以在中间件里面设置
# USER_AGENT = 'guazi_scrapy_project (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'

# Obey robots.txt rules
# robots.txt 搜索时遵循协议 一般设置为False
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 根据代理发送请求实际情况设置参数
CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 定义爬虫请求速度，一般0.1-0.5 或者1
DOWNLOAD_DELAY = 0.2
# 默认请求最大时间为180s
DOWNLOAD_TIMEOUT = 10

# 是否进行重试
RETRY_ENABLED = True
RETRY_TIMES = 3
# The download delay setting will honor only one of:
# 默认值为8
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 默认值为0
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 一般设置不开启
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 默认请求头
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'guazi_scrapy_project.middlewares.GuaziScrapyProjectSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'guazi_scrapy_project.middlewares.GuaziScrapyProjectDownloaderMiddleware': 543,
   'guazi_scrapy_project.middlewares.guazi_downloader_middleware': 500,
   'guazi_scrapy_project.middlewares.my_useragent': 501,
   'guazi_scrapy_project.middlewares.my_proxy': 502,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# 扩展中间件
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'guazi_scrapy_project.pipelines.GuaziScrapyProjectPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# 启用和配置HTTP缓存的敌方，默认是禁用
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
