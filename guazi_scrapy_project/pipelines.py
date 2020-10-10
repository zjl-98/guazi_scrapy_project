# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from handle_mongo import mongo

class GuaziScrapyProjectPipeline:
    def process_item(self, item, spider):
        mongo.save_data('guazi_data', item)
        return item
