import os
import pymongo

link = os.environ['MONGO_CONNECTION_STRING']


class MongoRepository:

    def get_all_documents(self):
        client = pymongo.MongoClient(link)
        db = client["user_shopping_list"]
        annotations_collection = db["annotations"]
        for x in annotations_collection.find():
            yield {
                "id": str(x["_id"]),
                "text": x["text"],
                "name": x["name"]
            }
