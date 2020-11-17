import xml
import os
import spacy
import zipfile
from pymongo import MongoClient
from flask import Flask
import xml.etree.ElementTree as ET
import itertools
import hashlib

def hash_model():
    openedFile = open(os.path.join('models', 'chemner', 'ner', 'model'))
    readFile = openedFile.read
    md5Hash = hashlib.md5(readFile)
    md5Hashed = md5Hash.hexdigest()
    return md5Hashed


def get_ner(document):

    fulltext = document['fulltext']

    nlp = spacy.load(os.path.join('models', 'chemner'))

    ners = [ nlp(unicode(x)).ents for x in fulltext ]
