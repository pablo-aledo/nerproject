from pymongo import MongoClient
from config.config import mongohost

def persist_data(application, year, title, abstract, fulltext):
    client = MongoClient(host=mongohost)

    db = client['nerproject']
    collection = db['patents']

    entry = {
          "application": application,
          "year": year,
          "title": title,
          "abstract": abstract,
          "fulltext": fulltext
          }

    collection.update({"application": application}, entry, upsert=True)

def get_patent( patentId ):

    client = MongoClient(host=mongohost)

    db = client['nerproject']
    collection = db['patents']

    document = collection.find_one({"application": patentId})

    return document

def save_ner(ners, hash_model):

    client = MongoClient(host=mongohost)

    db = client['nerproject']
    collection = db['ners']

    ner_document = {
          "modelId": hash_model,
          "ners": ners
    }

    collection.update({"modelId": hash_model}, ner_document, upsert=True)
