# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random
import re

import execjs
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class GuaziScrapyProjectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GuaziScrapyProjectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        """
            return None：
            scarpy继续执行request（保存执行下面的包含process_request方法的类，
            直到得到response对象
        """
        # - return None: continue processing this request
        """ 
            return a Response object：
            更低优先级的process_request和process_exception停止执行，
            转到执行process_response
        """
        # - or return a Response object
        """ 
            return a Request object：
            更低优先级的process_request停止执行,request重新放入调度器中
        """
        # - or return a Request object
        """ 
            raise IgnoreRequest：
            如果返回异常，所有的process_exception方法都会回调
            如果异常一直没被处理，就会被忽略
            errback
        """
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    # 当下载器从response到spider
    # request：request对象，当前response对应的request
    # response：当前进行的response
    # spider
    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        """
            return a Response object:
            更低优先级的process_response会继续执行
        """
        # - return a Response object
        """
            return a Response object:
            更低优先级的process_response不会被继续调用
            而是放到调用队列中，有process_request方法依次顺序处理
        """
        # - return a Request object
        """
            raise IgnoreRequest:
            若抛出异常，不会进入process_exception方法中
            会被errback方法回调
        """
        # - or raise IgnoreRequest
        return response

    # request: 产生异常的request
    # exception：当前抛出异常的exception
    # spider：当前exception的spider
    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        """
            return None:
            更低优先级的process_exception会被继续调用
        """
        # - return None: continue processing this exception
        """
            return a Response object:
            更低优先级的process_exception不会被继续调用
            process_response被调用
        """
        # - return a Response object: stops process_exception() chain
        """
            return None:
            更低优先级的process_exception不会被继续调用
            request被放入调度器中
        """
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class guazi_downloader_middleware(object):
    """ 自定义中间下载器 """
    def __init__(self):
        # 读取提前获取到的js
        with open('guazi.js', 'r') as f:
            self.f_read = f.read()

    def process_response(self, request, response, spider):
        if '正在打开中,请稍后' in response.text:
            # 定义正则表达式获取anti的两个值
            request_search = re.compile(r"anti\('(.*?)','(.*?)'\);")
            string = request_search.search(response.text).group(1)
            key = request_search.search(response.text).group(2)
            # 使用execjs解析js文件
            js = execjs.compile(self.f_read)
            # 调用js中的方法，并传值
            js_return = js.call('anti', string, key)
            # 重新拼接cookie
            cookie_value = {'antipas': js_return}
            # 将cookie添加到header中
            # print("当前使用的cookie是：%s" % cookie_value)
            request.cookies = cookie_value
            # 把请求放回调度器
            return request
        elif response.status == 200:
            return response
        elif '客官请求太频繁了' in response.text:
            return request


class my_useragent(object):
    def process_request(self, request, spider):
        # 网上找的user_agent,封装成了一个列表
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        # random.choice随机的选取列表中的一个数据
        agent = random.choice(user_agent_list)
        # request.headers，设置了请求头
        request.headers['User-Agent'] = agent


class my_proxy(object):
    def process_request(self, request, spider):
        # proxy，主机头和端口号
        request.meta['proxy'] = 'u5428.b5.t.16yun.cn:6460'
        # 用户名:密码,当前代理必须要有费用
        # 你自己买的代理，用户名和密码肯定和我的不一样
        proxy_name_pass = '16ODVGUF:875796'.encode('utf-8')
        encode_pass_name = base64.b64encode(proxy_name_pass)
        # 将代理信息设置到头部去
        # 注意！！！！！Basic后面有一个空格
        request.headers['Proxy-Authorization'] = 'Basic '+encode_pass_name.decode()
