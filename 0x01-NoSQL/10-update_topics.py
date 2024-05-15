#!/usr/bin/env python3
"""
Use pymongo to interact with mongod
"""


def update_topics(mongo_collection, name, topics):
    """
    Update a collection parameter, based on the name name
    and upadte the topics with the topics
    Parameters:
    -----------
    mongo_collection: a mongo collection object to update
    name: filter by the name=name
    topics: the new topics to replace the old one

    Returns:
    None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
