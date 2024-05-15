#!/usr/bin/env python3
"""
Use pymongo to interact with mongod
"""


def schools_by_topic(mongo_collection, topic):
    """
    Get a list of school having a specific topics
    Parameters:
    -----------
    mongo_collection: mongo collection object
    topic: a topic to filter on

    Return:
    -----------
    result: list of the founded collections
    """
    if not mongo_collection:
        return []
    result = mongo_collection.find({"topics": topic})

    return result
