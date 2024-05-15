#!/usr/bin/env python3
"""
Use pymongo to interact with mongod
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new documnet in a collection based on kwargs
    parameters:
    -----------
    mongo_collection: the mongo collection to insert into
    kwargs: the parameters of the new document

    Returns:
    ----------
    _id: the id of the new collection
    """
    if not kwargs or not isinstance(kwargs, dict):
        return

    _id = mongo_collection.insert_one(kwargs)

    return _id.inserted_id
