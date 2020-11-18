import os
import zipfile
from flask import Flask

from processPatent.processPatent import get_fulltext, get_application, get_year, get_title, get_abstract
from database.database import persist_data, get_patent, save_ner
from namedEntityRecognition.namedEntityRecognition import hash_model, get_ner
from config.config import basedir
from sparkLauncher.sparkLauncher import launch_spark

def loadArchive( zipName ):
    # with zipfile.ZipFile(os.path.join('data', 'uspat1_201831_back_80001_100000.zip'), 'r') as zip_ref:
        # zip_ref.extractall(os.path.join('tmp'))

    with open(os.path.join(basedir, 'tmp', 'US06179885B2.xml')) as file:
        data = file.read().replace('<br/>','')

    application = get_application(data)
    year = get_year(data)
    title = get_title(data)
    abstract = get_abstract(data)
    fulltext = get_fulltext(data)

    persist_data(application, year, title, abstract, fulltext)

    document = get_patent(application)
    ner = get_ner( document )
    save_ner( ner, hash_model() )

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/load/<zipId>')
def load_archive(zipId):
    loadArchive(zipId)
    return 'zip loaded %s' % zipId


