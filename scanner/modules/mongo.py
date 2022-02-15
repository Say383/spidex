import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017",
                                username="root",
                                password="test",
                                authSource="admin",
                                authMechanism='SCRAM-SHA-1')
database = client["TEST"]
collection = database["example"]
