import pymongo


class Database(object):
    uri = "mongodb://127.0.0.1/27017"
    DATABASE = None

    @staticmethod
    def initalise():
        client = pymongo.MongoClient(Database.uri)

        # Name of the database
        Database.DATABASE = client['PythonProjects']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)
