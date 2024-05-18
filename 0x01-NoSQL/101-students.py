#!/usr/bin/env python3
"""
Use pymongo to interact with mongod
"""
import pymongo


def top_students(mongo_collection):
    """
    Return all the students sorted by average score
    parameters:
    -----------
    mongo_collection: pymongo collection object

    returns:
    -----------
    list: list of all students sorted by average score
    """

    for doc in mongo_collection.find():
        sumation = [topic['score'] for topic in doc['topics']]
        ava = sum(sumation) / len(sumation)
        mongo_collection.update(
            {"_id": doc['_id']},
            {"$set": {"averageScore": ava}}
        )

    sorted_students = mongo_collection.find().sort(
        "averageScore", pymongo.DESCENDING)
    return sorted_students
