import os
import zipfile
from flask import Flask

from processPatent.processPatent import get_fulltext, get_application, get_year, get_title, get_abstract
from database.database import persist_data, get_patent, save_ner
from namedEntityRecognition.namedEntityRecognition import hash_model, get_ner
from config.config import basedir

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

    subprocess.call( [
        '/tmp/spark-3.0.1-bin-hadoop2.7/bin/spark-submit',
        '--deploy-mode', 'cluster',
        '--master', 'k8s://https://localhost:8443',
        '--name', 'sparkpi',
        '--conf', 'spark.kubernetes.authenticate.driver.serviceAccountName=spark',
        '--conf', 'spark.kubernetes.authenticate.submission.oauthToken=eyJhbGciOiJSUzI1NiIsImtpZCI6IlVJdFRxTHNHb294NXB2OVRyZzgzZVZzRm5QMHVWbGxRYVlYZmdlUlZUNzQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InNwYXJrLXRva2VuLXN6MmQ3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6InNwYXJrIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZjg2MThmZGUtN2ZmZi00NjkwLTk0M2YtMWM2M2ZkYzY1OGVmIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6c3BhcmsifQ.MNc2WOmUTE7qZocIBM9U61wnDD31aKCKSqHSQsGEmIQFMymOqO5VBkJuHidnHqR-lvWBeEupz1td6JTUbU6nDiFIUwGTO3c4Jy4iByeW4jKeA4zP60Mx6MwWcwjgTCMFtKLCiC86vQlNSLq4v2aD0KLiIozcqHpU9tz2G81MHoP5l-OuKhSrhQcxE3uZEdg2gRUUAP5_k33rAhQZbdNSGj_jl_GJDLLZmnZwlhuBX1ARiinyE7Raiq8n01eAJ8grLz0NEjR4qpSZoqiI-ZSV3uTxvTuJt_BC5aWuGY2f7h93Ba2XwPed4nSa0ndWP7ra0p2L4CcoAu5h0rCxU2eWqQ',
        '--conf', 'spark.executor.instances=5',
        '--conf', 'spark.kubernetes.driver.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.executor.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.container.imagePullPolicy=IfNotPresent',
        'local:///opt/spark/examples/src/main/python/pi.py',
        '100'
    ] )

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/load/<zipId>')
def load_archive(zipId):
    loadArchive(zipId)
    return 'zip loaded %s' % zipId


