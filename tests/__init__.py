import pymongo

from configuration import Configuration

mongo_client = pymongo.MongoClient(host=Configuration.mongo_host)
