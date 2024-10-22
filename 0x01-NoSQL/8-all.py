#!/usr/bin/env python3
""" 8-all.py """
import pymongo


def list_all(mongo_collection):
    """ lists all documents in a collection. """
    docList = []
    docs = mongo_collection.find()
    for doc in docs:
        docList.append(doc)
    return docList
