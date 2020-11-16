BASF Coding Challenge Backend Dev
=================================

This coding challenge allows you to showcase your technical skills and expertise.
The description is fuzzy on purpose. Of course, we don’t expect you to create a perfect solution, but
we are curious about your approach and your ideas.

Task
---

You are asked to implement a simple information extraction pipeline that should try to extract
chemicals (like isobutanol) from a set of patents. This means, your pipeline should

1. read an archive file of patents
2. take metadata (application, year, title), abstract and full-text of each patent into account
3. persist metadata and abstract in a database
4. run Named Entity Recognition (NER) over the abstract and full-text
5. persist the NEs in the database.

The pipeline should be callable via a REST endpoint, but it needs to have only the most basic
operations, i.e. load an archive and delete the database.

Please use Python or Java (or Scala or Kotlin) and also use any framework and libraries that you
would also use in a real-world, production use-case.
For persistence, you may use MongoDB or any other database. In case you use MongoDB, you can
assume it runs with standard configuration at runtime (i.e. we will provide it at runtime.)
For the NER, you may use Spacy (Python) or Standord CoreNLP (Java) or other suitable approaches.
Please consider that your code should of course not only run on this single archive, which is just on
very small sample of the data. In production, we would have at least 10,000 archives.

Data Input
----------

You can access one sample archive from here:

https://hiringchallenges.blob.core.windows.net/patents/uspat1_201831_back_80001_100000.zip?st=2020-10-21T10%3A18%3A37Z&amp;se=2020-11-29T23%3A00%3A00Z&amp;sp=rl&amp;sv=2018-03- 28&amp;sr=b&amp;sig=TPKloJtepmYeo1laBsSy0sj8A6dKEzzHLWmZXaexWlU%3D

Bonus Task
----------

In case you started enjoying this challenge, here’s a bonus task (it is really optional):
The pipeline above extracts any kind of named entity and is not specific to chemicals obviously. There
are two things you could to do about that (or just one of them):

(a) Replace the generic NER software with something specific to Chemical NER (ChemNER),
(b) Evaluate the results of the initial NER, by comparing the output from our database against a

list of known chemicals
-----------------------

There are different options how to get list of all know chemicals, Wikipedia is good enough for this
challenge. For getting the data, you may query Wikidata (e.g. via SPARQL 1 ) or download a datasets of
CSV tables from DBpedia 2 , or take any other easy to do approach.

Deliverables
------------

Please provide us with

(a) your code as github repo (otherwise as local git repo via email)
(b) a readme explaining how to (easily, pls) run your software
(c) a brief textual description

a. explaining your technology and design decisions w.r.t the functional and non-
functional requirements
b. discussion potential challenges w.r.t. scalability and maintainability (in particular for
changes in data volumes and formats)
