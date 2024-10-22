#!/usr/bin/env python3
""" 8-all.py """
import pymongo


def list_all(mongo_collection):
    """ lists all documents in a collection. """
    if not mongo_collection:
        return []
    for doc in mongo_collection.find():
        return [doc]
