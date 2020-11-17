import xml
import os
import spacy
import zipfile
from pymongo import MongoClient
from flask import Flask
import xml.etree.ElementTree as ET
import itertools
import hashlib

def get_fulltext(data):
    root = ET.fromstring(data)
    element = root; element
    element = element.find('description'); element
    element = element.findall('p'); element
    element = [ x.text for x in element ]; element
    element = [ x.split('\n') for x in element ]; element
    element = list(itertools.chain(*element)); element
    element = [ x.strip() for x in element ]; element
    element = [ x for x in element if 'isobutanol' in x ]; element
    #element = [ element[10] ]; element
    return element

def get_application(data):
    root = ET.fromstring(data)
    element = root; element
    element = element.find('bibliographic-data'); element
    element = element.find('application-reference'); element
    element = element.find('document-id'); element
    element = element.find('doc-number'); element
    element = element.text; element
    return element

def get_year(data):
    root = ET.fromstring(data)
    element = root; element
    element = element.find('bibliographic-data'); element
    element = element.find('publication-reference'); element
    element = element.find('document-id'); element
    element = element.find('date'); element
    element = element.text; element
    element = element[0:4]; element
    return element

def get_title(data):
    root = ET.fromstring(data)
    element = root; element
    element = element.find('bibliographic-data'); element
    element = element.find('invention-title'); element
    element = element.text; element
    return element

def get_abstract(data):
    root = ET.fromstring(data)
    element = root; element
    element = element.find('abstract'); element
    element = element.getchildren(); element
    element = element[0]; element
    element = element.text; element
    element = element.split('\n'); element
    element = filter( lambda x : x.strip() != '', element ); element
    element = [ x.strip() for x in element ]; element
    return element

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

def hash_model():
    openedFile = open(os.path.join('models', 'chemner', 'ner', 'model'))
    readFile = openedFile.read
    md5Hash = hashlib.md5(readFile)
    md5Hashed = md5Hash.hexdigest()
    return md5Hashed

def process_patent( patentId ):

    client = MongoClient()

    db = client['patents']
    input_collection = db['collection']
    output_collection = db['ners']

    document = input_collection.find_one({"application": u'09337997'})

    fulltext = document['fulltext']

    nlp = spacy.load(os.path.join('models', 'chemner'))

    ners = [ nlp(unicode(x)).ents for x in fulltext ]
    ner_document = {
          "modelId": hash_model(),
          "ners": ners
    }

    output_collection.insert_one(ner_document)

def loadArchive( zipName ):
    # with zipfile.ZipFile(os.path.join('data', 'uspat1_201831_back_80001_100000.zip'), 'r') as zip_ref:
        # zip_ref.extractall(os.path.join('tmp'))

    with open(os.path.join('tmp', 'US06179885B2.xml')) as file:
        data = file.read().replace('<br/>','')

    application = get_application(data)
    year = get_year(data)
    title = get_title(data)
    abstract = get_abstract(data)
    fulltext = get_fulltext(data)

    persist_data(application, year, title, abstract, fulltext)
    process_patent( application )

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/load/<zipId>')
def load_archive(zipId):
    loadArchive(zipId)
    return 'zip loaded %s' % zipId


