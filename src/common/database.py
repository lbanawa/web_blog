import pymongo

__author__ = 'laurenbanawa'

class Database(object):
    # Universal Resource Identifier allows program to find and connect with the process
    # use the same URI for all objects in Database, this is why it is directly under the class
    # these variables are uppercase to tell programmers not to change these, these are constant through our program
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    # the object needs to be able to do things, and these actions are defined as methods inside the class
    #   for each object to have access to
    # @staticmethod makes a method that does not affect a specific object -- should be executed at the class level
    @staticmethod
    def initialize():
        # MongoClient gives us the functionality to interact with MongoDB
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    # insert data into the database
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    # within the database, find a list of all elements matching certain criteria
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    # within the database, find one element -- example: searching for one specific user
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)