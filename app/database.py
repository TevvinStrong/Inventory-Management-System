# app/database.py

from pymongo import MongoClient

class ProductDatabase:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_product(self, product_data):
        self.collection.insert_one(product_data)
