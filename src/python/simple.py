import xml
import os
import spacy
import zipfile
from pymongo import MongoClient

with zipfile.ZipFile(os.path.join('data', 'uspat1_201831_back_80001_100000.zip'), 'r') as zip_ref:
    zip_ref.extractall(os.path.join('data', 'uspat1_201831_back_80001_100000'))

with open(os.path.join('data', 'uspat1_201831_back_80001_100000', 'US06179885B2.xml')) as file:
    data = file.read().replace('<br/>','')

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

nlp = spacy.load(os.path.join('models', 'chemner'))

[ nlp(unicode(x)).ents for x in element ]

root = ET.fromstring(data)
element = root; element
element = element.find('abstract'); element
element = element.getchildren(); element
element = element[0]; element
element = element.text; element
element = element.split('\n'); element
element = filter( lambda x : x.strip() != '', element ); element
element = [ x.strip() for x in element ]; element

client = MongoClient()

db = client['namedEntityRecognition']
collection = db['patents']

entry1 = {
      "application": "06176565",
      "year": "2001",
      "title": "Cleaning member for ink jet head and ink jet apparatus provided with said cleaning member",
      "abstract": ["paragraph-1", "paragraph-2" ],
      "fulltext": ["paragraph-1", "paragraph-2" ]
      }

db.collection.insert_one(entry1)
