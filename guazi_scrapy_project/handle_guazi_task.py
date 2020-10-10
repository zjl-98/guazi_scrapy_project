import json

import requests
import execjs
import re

from handle_mongo import mongo

# 要爬取数据的网址
url = 'https://www.guazi.com/www/buy'

# 请求头信息
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.guazi.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
}
city_header = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.guazi.com",
    "Referer": "https://www.guazi.com/www/buy",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

# 发起请求
response = requests.get(url=url, headers=header)
# 设置编码
response.encoding = 'utf-8'
if '正在打开中,请稍后' in response.text:
    # 定义正则表达式获取anti的两个值
    request_search = re.compile(r"anti\('(.*?)','(.*?)'\);")
    string = request_search.search(response.text).group(1)
    key = request_search.search(response.text).group(2)

    # 读取提前获取到的js
    with open('guazi.js', 'r') as f:
        f_read = f.read()

    # 使用execjs解析js文件
    js = execjs.compile(f_read)

    # 调用js中的方法，并传值
    js_return = js.call('anti', string, key)

    # 重新拼接cookie
    cookie_value = 'antipas=' + js_return

    # 将cookie添加到header中
    header['Cookie'] = cookie_value
    city_header['Cookie'] = cookie_value

    # 再次发起请求
    response_second = requests.get(url=url, headers=header)

    # 由于城市是用js存放，所以需要再请求一次
    city_url = 'https://www.guazi.com/www/?act=ajaxGetOpenCity'
    response_third = requests.get(url=city_url, headers=city_header)

    # 设置编码
    response_third.encoding = 'utf-8'

    # json格式key获取所属值
    city_json = json.loads(response_third.text)['data']
    city_list = city_json['cityList']['all']

    # TODO: 正则匹配获取车品牌
    brand_search = re.compile(r'href="\/www\/(.*?)/c-1/#bread"\s+>(.*)</a>')
    brand_list = brand_search.findall(response_second.text)
    # TODO: 双重循环定义链接
    for i in city_list:
        for city_item in city_list[i]:
            if city_item['domain'] == 'bj':
                for brand_item in brand_list:
                    # https://www.guazi.com/anji/buy
                    # https://www.guazi.com/anji/audi
                    # https://www.guazi.com/anji/audi/o1i7/#bread
                    info = {
                        'task_url': 'https://www.guazi.com/' + city_item['domain'] + '/' + brand_item[0] + '/o1i7',
                        'city_name': city_item['name'],
                        'brand_name': brand_item[1],
                        'item_type': 'list_item'
                    }
                    mongo.insert_mongo('guazi_task', info)
