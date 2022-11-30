import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities
from Validator import Validator


if __name__ == '__main__':

    # connect
    client : MongoClient = Utilities.startup()

    # initialize
    client.drop_database('key_hook')
    db = client.key_hook

    employees = db.employees
    room_requests = db.room_requests
    key_issue = db.key_issue
    key_issue_return = db.key_issue_return
    key_issue_loss = db.key_issue_loss

    # unique constraint
    employees.create_index([
        ('id', pymongo.ASCENDING)
    ], unique=True)
    room_requests.create_index([
        ('request_id', pymongo.ASCENDING)
    ], unique=True)
    key_issue.create_index([
        ('issue_number', pymongo.ASCENDING)
    ], unique=True)
    key_issue_return.create_index([
        ('issue_number', pymongo.ASCENDING)
    ], unique=True)
    key_issue_loss.create_index([
        ('issue_number', pymongo.ASCENDING)
    ], unique=True)

    # validator
    db.command('collMod', 'employees', validator=Validator.employees_validator())

    employees.insert_one({
        'id': 1,
        'full_name': 'james bon'
    })