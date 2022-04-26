import pymongo
from datetime import datetime

# Mongodb related functions
def connect_to_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.aprioriPlatform
    return db


def store_results(id: str, data: dict):
    # print(data.keys())
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
    print(data)
    return data

