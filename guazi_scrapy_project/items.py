# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # 根据车源号去重
    car_id = scrapy.Field()
    # 车名
    car_name = scrapy.Field()
    # 从哪里抓取过来的数据
    from_url = scrapy.Field()
    # 车价
    car_price = scrapy.Field()
    # 上牌时间
    license_time = scrapy.Field()
    # 上牌地
    # license_place = scrapy.Field()
    # 里程
    km_info = scrapy.Field()
    # 排量信息
    displacement_info = scrapy.Field()
    # 变速箱 手动还是自动
    transmission_case = scrapy.Field()
