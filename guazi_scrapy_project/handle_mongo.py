from pymongo import MongoClient


class HandleMongo(object):
    """ 定义Mongo类"""
    def __init__(self):
        my_client = MongoClient("mongodb://192.168.43.76:27017")
        self.my_db = my_client['db_guazi']

    # 存储task的逻辑
    def insert_mongo(self, collection_name, task):
        print("当前存储的task是%s: " % task)
        my_collection = self.my_db[collection_name]
        task = dict(task)
        my_collection.insert_one(task)

    # 查询数据
    def find_mongo(self, collection_name):
        my_collection = self.my_db[collection_name]
        task = my_collection.find_one_and_delete({})
        return task
    
    # 保存data数据
    def save_data(self, collection_name, data):
        print("当前存储的data是%s: " % data)
        my_collection = self.my_db[collection_name]
        task = dict(data)
        my_collection.update({'car_id': data['car_id']}, data, True)


mongo = HandleMongo()