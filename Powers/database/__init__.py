from sys import exit as exiter

from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError

from KeysSecret import DB_NAME, DB_URI

try:
    db_client = MongoClient(DB_URI)
except PyMongoError as f:
    print(f"Error in DB: {f}")
    exiter(1)
main_db = db_client[DB_NAME]

class MongoDB:
    def __init__(self, collection) -> None:
        self.collection = main_db[collection]

    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    def find_one(self, query):
        result = self.collection.find_one(query)
        if result:
            return result
        return False

    def find_all(self, query=None):
        if query is None:
            query = {}
        return list(self.collection.find(query))


    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)


    def delete_one(self, query):
        self.collection.delete_many(query)
        return self.collection.count_documents({})


    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new


    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document
    
    def sort_by(self):
        set_sorted = set()
        sort = self.collection.find()
        for i in sort:
            set_sorted.add(i['type'])
        return list(set_sorted)
