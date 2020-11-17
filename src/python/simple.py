import xml
import os
import spacy
import zipfile
from pymongo import MongoClient
from flask import Flask


def get_description(data):
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

def loadArchive( zipName )
    with zipfile.ZipFile(os.path.join('data', 'uspat1_201831_back_80001_100000.zip'), 'r') as zip_ref:
        zip_ref.extractall(os.path.join('tmp', 'uspat1_201831_back_80001_100000'))

    with open(os.path.join('tmp', 'uspat1_201831_back_80001_100000', 'US06179885B2.xml')) as file:
        data = file.read().replace('<br/>','')

    application = get_application(data)
    year = get_year(data)
    title = get_title(data)
    description = get_description(data)
    abstract = get_abstract(data)
    fulltext = get_fulltext(data)

    persist_data(application, year, title, description, abstract, fulltext)

    nlp = spacy.load(os.path.join('models', 'chemner'))

    [ nlp(unicode(x)).ents for x in element ]

app = Flask(__name__)

@app.route('/load/<zipId>')
def show_user_profile(zipId):
    loadArchive(zipId)
    return 'zip loaded %s' % escape(zipId)

if __name__ == '__main__':
    app.run
