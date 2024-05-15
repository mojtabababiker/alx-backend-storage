#!/usr/bin/env python3
"""
Using pymongo to interact with mongod
"""


def list_all(mongo_collection):
    """
    Find all the documnets on the mongo_collection object
    Parameters:
    -----------
        mongo_collection: pymongo collection object
    Returns:
    -----------
        result: list of all the founded documents, or []
                no ones founded
    """
    if not mongo_collection:
        return []
    try:
        result = mongo_collection.find()
        return result
    except Exception as e:
        print(e)
        return []
