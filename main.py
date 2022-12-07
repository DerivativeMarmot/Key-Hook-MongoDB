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


def main_menu(db):
    choice = -1
    while choice != 0:
        print(
            "Menu options:\n1.\tCreate a key\n2.\tEmployee Room Request\n3.\tIssue a key\n4.\tLosing a key\n5.\tRooms "
            "employee can enter\n6.\t"
            "Delete Key\n7.\tDelete Employee\n8.\tAdd Door to a hook\n9.\tUpdate Access Request\n"
            "10.\tEmployees that can enter a room\n0.\tExit")
        choice = int(input("Your Choice: "))
        print()

        if choice == 1:
            print("Which hook would you like to apply to this key?")

            hook_col = db.hooks
            all_hooks = hook_col.find({})
            option = 0
            for hook in all_hooks:
                print(f"Option {option}: Hook Number {hook.hook_number}")
                option += 1
            response = int(input("Your Choice: "))
            hook = all_hooks[response]
            keys = db.keys.find({"hook": DBRef("hooks", hook["_id"])})
            new_key = {"key_number": len(keys)+1,
                       "hook": DBRef("hooks", hook["_id"])}
            result = db.keys.insert_one(new_key)
            print(f"New key, #{new_key['key_number']} successfully added for hook {hook['hook_number']}")
            print()

        elif choice == 2:
            print("Which employee is requesting the access?")
            emps = db.employees.find({})
            option = 0
            for emp in emps:
                print(f"{option}: Full name {emp['full_name']}, id: {emp['_id']}")
                option += 1
            response = int(input("Your Choice: "))
            emp = emps[response]

            print("Which room are you requesting access for?")
            rooms = db.rooms.find({})
            option = 0
            for room in rooms:
                print(f"{option}: {db.dereference(room['building'])['name']} {room['room_number']}")
                option += 1
            response = int(input("Your Choice: "))
            room = rooms[response]

            new_request = {"request_time": datetime.now(),
                           "employee": emp,
                           "room": room}
            result = db.room_requests.insert_one(new_request)
            print("New request successfully made.")
            print()

        elif choice == 3:
            pass
        elif choice == 4:
            pass
        elif choice == 5:
            pass
        elif choice == 6:
            pass
        elif choice == 7:
            pass
        elif choice == 8:
            pass
        elif choice == 9:
            pass
        elif choice == 10:
            pass
        else:
            print("Exiting Application ... ")


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

    main_menu(db)
    

    