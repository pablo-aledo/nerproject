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
