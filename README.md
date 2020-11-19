BASF Coding Challenge Backend Dev
=================================

This is my solution to the BASF Coding challenge for Backednd Developer.

Summary
-------

The given project reads patents from zip archives, extracts chemicals from them
and persists the information in a MongoDB database.

1. read an archive file of patents -> /decompress endpoint
2. take metadata (application, year, title), abstract and full-text of each patent into account -> /persist endpoint
3. persist metadata and abstract in a database -> /persist endpoint
4. run Named Entity Recognition (NER) over the abstract and full-text -> /ner endpoint
5. persist the NEs in the database. -> /ner endpoint

Data Input
----------

There is a script to download the input data in /data folder. zip archives have
to be stored in a persistent volume.

Bonus Task
----------

Code to train and test ChemNER performance is provided. It can be adapted to
consider more chemicals besides isobutanol.

Selection of technologies
-------------------------

- **Python** is used as the main programming language
- **Flask** is used as service provider
- **Kubernetes** is used as orchestration framework
- **Docker** is used as container solution
- **spacy** is used as NER library
- **Spark** is used as parallelization library

Deliverables
------------

Please provide us with

(a) your code as github repo (otherwise as local git repo via email) -> This repository
(b) a readme explaining how to (easily, pls) run your software -> This README
(c) a brief textual description -> This README

Installation
------------

This program is meant to be used in a k8s cluster.

- Create a k8s cluster
- create a service account for the spark user in the k8s cluster ``` k create serviceaccount spark ```
- create a clusterrolebinding created service account ``` k create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default ```
- train the ChemNER model using train.py and store the model in the /model folder
- modify config.py indicating the endpoint of the k8s API as well as the token for the spark service account
- create docker images with Dockerfiles provided in deployment/Docker
- Deploy the solution to the k8s cluster with the templates provided in deployment/templates. These templates include the creation of a persistent volume for storing the data, and a service for MongoDB as well as the rest API
- Store the zip archives with patents in the created persistent volume
- the project exposes a rest API associated to a the nerserver svc
- The service can be queried with (for example) curl ``` curl -v http://localhost:5000/decompress/uspat1_201831_back_80001_100000.zip ```

