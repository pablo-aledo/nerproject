import os
import zipfile
from flask import Flask

from processPatent.processPatent import get_fulltext, get_application, get_year, get_title, get_abstract
from database.database import persist_data, get_patent, save_ner
from namedEntityRecognition.namedEntityRecognition import hash_model, get_ner
from config.config import basedir
from sparkLauncher.sparkLauncher import launch_spark

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/decompress/<zipId>')
def decompress(zipId):
    with zipfile.ZipFile(os.path.join(basedir, 'data', zipId), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(basedir, 'tmp'))
    return 'zip loaded %s' % zipId

@app.route('/persist/<patentId>')
def persist(patentId):
    with open(os.path.join(basedir, 'tmp', patentId)) as file:
        data = file.read().replace('<br/>','')

    application = get_application(data)
    year = get_year(data)
    title = get_title(data)
    abstract = get_abstract(data)
    fulltext = get_fulltext(data)

    persist_data(application, year, title, abstract, fulltext)
    return 'patent stored in the databse %s' % patentId

@app.route('/ner/<patentId>')
def ner(patentId):
    document = get_patent(patentId)
    ner = get_ner( document )
    save_ner( ner, hash_model() )
    return 'NER computed %s' % patentId

@app.route('/sparkner')
def sparkner():
    launch_spark()
    return 'spark launched'
