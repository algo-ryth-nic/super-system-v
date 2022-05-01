import pymongo
from datetime import datetime
import json

# Mongodb related functions
def connect_to_mongo():
    client = pymongo.MongoClient('mongodb', 27017)
    db = client.userdatassv
    return db


def store_results(id: str, data: dict):
    # print(type(id))
    db = connect_to_mongo()
    results = db.apriori_results
    results.insert_one({
        '_id': id,
        'datetime': datetime.now(),
        'frequent_items': data['freq_items'],
        'association-rules': data['rules']
    })


def get_results(id: str):
    db = connect_to_mongo()
    results = db.apriori_results
    data = results.find_one({'_id': id})
    # print(data)
    return data


if __name__ == "__main__":
    # store_results('2', {'freq_items': [], 'rules': []})
    # print(get_results('2'))
    pass