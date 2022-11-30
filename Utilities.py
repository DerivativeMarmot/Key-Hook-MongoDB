from pymongo import MongoClient

class Utilities:
    @staticmethod
    def startup():
        cluster = ''
        client = MongoClient(cluster)
        return client
