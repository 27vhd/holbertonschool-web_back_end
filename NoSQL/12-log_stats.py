#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
(database: logs, collection: nginx).
"""
from pymongo import MongoClient


def log_stats(collection):
    """
    Print the total number of logs, the count per HTTP method
    and the number of GET requests on the /status path.
    """
    print("{} logs".format(collection.count_documents({})))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))
    status = collection.count_documents({"method": "GET",
                                         "path": "/status"})
    print("{} status check".format(status))


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_stats(client.logs.nginx)