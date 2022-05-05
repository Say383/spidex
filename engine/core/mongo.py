import pymongo
from pymongo import errors
from loguru import logger
import os
import sys

def insert_data(devices):
    try:
        client = pymongo.MongoClient("{}".format(os.environ.get("MONGODB_URI")), username="{}".format(os.environ.get("MONGODB_USER")), password="{}".format(os.environ.get("MONGODB_PASS")), authSource="admin", authMechanism='SCRAM-SHA-1')
        database = client["IOT"]
        collection = database["device"]
        collection.insert_many(devices)
        logger.info("Data successfully inserted")

    except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError):
        logger.error("Could not establish connection with the database")
        sys.exit(1)
