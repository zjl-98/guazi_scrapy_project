import re

import scrapy

from guazi_scrapy_project.handle_mongo import mongo

from guazi_scrapy_project.items import GuaziScrapyProjectItem


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['guazi.com']
    # start_urls = ['http://guazi.com/']

    # 这个request对象代表了一个http的请求
    # 会经由downloader去执行，从而产生一个response
    def start_requests(self):
        while True:
            # 获取保存在Mongo中的task数据
            task = mongo.find_mongo('guazi_task')
            # 没有task时，停止
            if not task:
                break
            if '_id' in task:
                task.pop('_id')
            print("当前获取的task是：%s" % task)
            if task['item_type'] == 'list_item':
                # 发起get请求
                yield scrapy.Request(
                    url=task['task_url'],
                    callback=self.handle_car_item,
                    dont_filter=True,
                    errback=self.handle_err,
                    meta=task
                    # callback回调函数，默认不写会调用parse方法
                    # 请求方法，默认为get
                    # method='GET',
                    # 请求头信息
                    # headers=
                    # body=请求体
                    # cookies=要携带的cookie信息
                    # meta=是字典的格式，向其他方法里面传递信息
                    # encoding='utf-8'字符编码
                    # priority=0请求的优先级
                    # dont_filter=False这个请求是否要被过滤
                    # errback=self.handle_err,当程序处理请求返回有错误的时候，使用这个参数
                    # flags
                )

                #  发起post表单请求
                # yield scrapy.FormRequest(
                #
                # )
            elif task['item_type'] == 'list_info':
                yield scrapy.Request(url=task['car_url'], callback=self.handle_car_info, dont_filter=True, meta=task, errback=self.handle_err)

    # 报错回调方法
    def handle_err(self, failure):
        # 当前task访问失败后，重新将其保存到mongo中的task库中，再次请求
        # print(failure)
        mongo.insert_mongo('guazi_task', failure.request.meta)

    # 自定义解析方法
    def handle_car_item(self, response):
        if '中为您找到0辆好车' in response.text:
            return
        car_item_list = response.xpath("//ul[@class='carlist clearfix js-top']/li")
        for car_item in car_item_list:
            # 保存车名和详情页链接
            car_list_info = {
                "car_name": car_item.xpath("./a/h2/text()").extract_first(),
                "car_url": 'https://www.guazi.com' + car_item.xpath("./a/@href").extract_first(),
                'item_type': 'list_info'
            }
            # print(car_list_info)
            yield scrapy.Request(url=car_list_info['car_url'], callback=self.handle_car_info, dont_filter=True, meta=car_list_info, errback=self.handle_err)

        # 获取下一页数据
        if response.xpath("//ul[@class='pageLink clearfix']/li[last()]/a/span/text()") == '下一页':
            # 定义下一页正则匹配
            next_url_search = re.compile(r'https://www.guazi.com/(.*?)/(.*?)/o(\d+)i7')
            next_url_info = next_url_search.findall(response.url)[0]
            # 拼接下一页链接
            response.request.meta['task_url'] = 'https://www.guazi.com/%s/%s/o%si7' % (next_url_info[0], next_url_info[1], str(next_url_info[2] + 1))
            yield scrapy.Request(url=response.request.meta['task_url'], callback=self.handle_car_item, meta=response.request.meta, dont_filter=True, errback=self.handle_err)

    def handle_car_info(self, response):
        # 根据车源号去重
        car_id_search = re.compile(r'车源号：(.*?)\s+')
        car_info = GuaziScrapyProjectItem()
        car_info['car_id'] = car_id_search.search(response.text).group(1)
        # 车名
        car_info['car_name'] = response.request.meta['car_name']
        # 从哪里抓取过来的数据
        car_info['from_url'] = response.request.meta['car_url']
        # 车价
        car_info['car_price'] = response.xpath("//div[@class='price-main']/span/text()").extract_first().strip()
        # 上牌时间
        car_info['license_time'] = response.xpath("//ul[@class='assort clearfix']/li[@class='one']/span/img/@src").extract_first().strip()
        # 里程
        car_info['km_info'] = response.xpath("//ul[@class='assort clearfix']/li[@class='two']/span/text()").extract_first().strip()
        # 排量信息
        car_info['displacement_info'] = response.xpath("//ul[@class='assort clearfix']/li[@class='three']/span/text()").extract_first().strip()
        # 变速箱 手动还是自动
        car_info['transmission_case'] = response.xpath("//ul[@class='assort clearfix']/li[@class='last']/span/text()").extract_first().strip()
        yield car_info
