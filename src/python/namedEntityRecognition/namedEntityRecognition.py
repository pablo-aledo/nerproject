import spacy
import hashlib
import os

from config.config import basedir

def hash_model():
    basedir = '/opt/app/nerproject'
    with open(os.path.join(basedir, 'models', 'chemner', 'ner', 'model'), 'rb') as openedFile:
          readFile = openedFile.read()
    # openedFile = open(os.path.join(basedir, 'models', 'chemner', 'ner', 'model'))
    # readFile = openedFile.read()
    md5Hash = hashlib.md5(readFile)
    md5Hashed = md5Hash.hexdigest()
    return md5Hashed

def get_ner(document):

    fulltext = document['fulltext']

    nlp = spacy.load(os.path.join(basedir, 'models', 'chemner'))

    ners = [ nlp(unicode(x)).ents for x in fulltext ]

    return ners
