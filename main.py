import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities
from Validator import Validator
from datetime import datetime


if __name__ == '__main__':

    # connect
    client : MongoClient = Utilities.startup()

    # initialize
    if 'key_hook' in client.list_database_names():
        client.drop_database('key_hook')
    db = client.key_hook

    employees = db.employees
    room_requests = db.room_requests
    rooms = db.rooms
    key_issue = db.key_issue
    key_issue_return = db.key_issue_return
    key_issue_loss = db.key_issue_loss

    # unique constraint
    employees.create_index([
        ('full_name', pymongo.ASCENDING)
    ], unique=True)
    room_requests.create_index([
        ('request_time', pymongo.ASCENDING),
        ('employee', pymongo.ASCENDING),
        ('room', pymongo.ASCENDING),
    ], unique=True)
    key_issue.create_index([
        ('start_time', pymongo.ASCENDING),
        ('room_request', pymongo.ASCENDING),
        ('key', pymongo.ASCENDING)
    ], unique=True)
    key_issue_return.create_index([
        ('loss_date', pymongo.ASCENDING)
    ], unique=True)
    key_issue_loss.create_index([
        ('return_date', pymongo.ASCENDING)
    ], unique=True)

    # validator
    db.command('collMod', 'employees', validator=Validator.employees_validator())
    db.command('collMod', 'room_requests', validator=Validator.room_requests_validator())
    db.command('collMod', 'key_issue', validator=Validator.key_issue_validator())
    db.command('collMod', 'key_issue_return', validator=Validator.key_issue_return_validator())
    db.command('collMod', 'key_issue_loss', validator=Validator.key_issue_loss_validator())


    e1 = employees.insert_one({
        # 'id': 1,
        'full_name': 'james bon'
    })
    e2 = employees.insert_one({
        # 'id': 2,
        'full_name': 'james bone',
    })

    room1 = rooms.insert_one({
        'building_name': 'VEC',
        'room_number': 322
    })

    rq1 = room_requests.insert_one({
        'request_time': datetime.now(),
        'employee': DBRef('employees', e1.inserted_id),
        'room': DBRef('rooms', room1.inserted_id)
    })

    # ki1 = key_issue.insert_one({
    #     'start_time': datetime.now(),
    #     'room_request': , 
    #     'key'
    # })
    

    