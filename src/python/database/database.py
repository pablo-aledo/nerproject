from pymongo import MongoClient

def persist_data(application, year, title, abstract, fulltext):
    client = MongoClient()

    db = client['patents']
    collection = db['patents']

    entry = {
          "application": application,
          "year": year,
          "title": title,
          "abstract": abstract,
          "fulltext": fulltext
          }

    db.collection.insert_one(entry)

def get_patent( patentId ):

    client = MongoClient()

    db = client['patents']
    input_collection = db['collection']
    output_collection = db['ners']

    document = input_collection.find_one({"application": u'09337997'})

    return document

def save_ner(ners, hash_model):

    client = MongoClient()

    db = client['patents']
    output_collection = db['ners']
    ner_document = {
          "modelId": hash_model,
          "ners": ners
    }

    output_collection.insert_one(ner_document)
