import getpass
from datetime import datetime
from pprint import pprint

import pymongo
from bson import DBRef
from pymongo import MongoClient
from pprint import pprint
from Utilities import Utilities
from Validator import Validator
import Insert_Statements as IS
from datetime import datetime


def main_menu(db):
    choice = -1
    while choice != 0:
        print(
            "Menu options:\n\
            1.\tCreate a key\n\
            2.\tEmployee Room Request\n\
            3.\tIssue a key\n\
            4.\tLosing a key\n\
            5.\tRooms that a employee can enter\n\
            6.\tDelete Key\n\
            7.\tDelete Employee\n\
            8.\tAdd Door to a hook\n\
            9.\tUpdate Access Request\n\
            10.\tEmployees that can enter a room\n\
            0.\tExit"
        )
        choice = int(input("Your Choice: "))
        print()

        if choice == 1:
            print("Which hook would you like to apply to this key?")

            hook_col = db.hooks
            all_hooks = list(hook_col.find({}))
            option = 0
            for hook in all_hooks:
                print(f"Option {option}: Hook Number {hook['hook_number']}")
                option += 1
            response = int(input("Your Choice: "))

            hook = all_hooks[response]
            keys = list(db.keys.find({}))
            new_key = {"key_number": len(keys) + 1,
                       "hook": DBRef("hooks", hook["_id"])}
            result = db.keys.insert_one(new_key)
            print(f"New key, #{new_key['key_number']} successfully added for hook {hook['hook_number']}")
            print()

        elif choice == 2:
            print("Which employee is requesting the access?")
            emps = list(db.employees.find({}))
            option = 0
            for emp in emps:
                print(f"Option {option}: Full name: {emp['full_name']}, id: {emp['_id']}")
                option += 1
            response = int(input("Your Choice: "))
            emp = emps[response]

            print("Which room are you requesting access for?")
            rooms = list(db.rooms.find({}))
            option = 0
            for room in rooms:
                building = db.dereference(room['building'])
                print(f"Option {option}: {building['name']} {room['room_number']}")
                option += 1
            response = int(input("Your Choice: "))
            room = rooms[response]

            new_request = {"request_time": datetime.now(),
                           "employee": DBRef('employees', emp['_id']),
                           "room": DBRef('rooms', room['_id'])}
            result = db.room_requests.insert_one(new_request)
            print("New request successfully made.")
            print()

        elif choice == 3:
            print("What room request would you like to issue a key to?")
            requests = list(db.room_requests.find({}))
            option = 0
            for request in requests:
                emp = db.dereference(request['employee'])
                room = db.dereference(request['room'])
                building = db.dereference(room['building'])
                print(f"Option {option}: Employee Full name {emp['full_name']},"
                      f" Requesting: {building['name']} {room['room_number']}")
                option += 1
            response = int(input("Your Choice: "))
            request = requests[response]
            emp = db.dereference(request['employee'])
            requested_room = db.dereference(request['room'])

            hdos = db.hook_door_opening.find({})
            for hdo in hdos:
                door = db.dereference(hdo['door'])
                room = db.dereference(door['room'])
                if room == requested_room:
                    hook = db.dereference(hdo['hook'])
                    # create a new key under that hook
                    keys = list(db.keys.find({}))
                    new_key = db.keys.insert_one({"key_number": len(keys) + 1,
                                                  "hook": DBRef("hooks", hook["_id"])})
                    result = db.key_issue.insert_one({
                        "start_time": datetime.now(),
                        "room_request": DBRef("room_requests", request['_id']),
                        "key": DBRef('keys', new_key.inserted_id)
                    })
                    print("A key has been created and issued to the room request")
                    break

        elif choice == 4:
            print("Which key has been lost?")
            key_issues = list(db.key_issue.find({}))
            option = 0
            for key_issue in key_issues:
                room_request = db.dereference(key_issue['room_request'])
                room = db.dereference(room_request['room'])
                building = db.dereference(room['building'])
                print(f"Option {option}: Key Issue ID {key_issue['_id']} for {building['name']} {room['room_number']}")
                option += 1
            response = int(input("Your Choice: "))
            issue = key_issues[response]
            new_loss = {
                "loss_date": datetime.now(),
                "key_issue": DBRef("key_issue", issue['_id'])
            }
            db.key_issue_loss.insert_one(new_loss)
            print("Key loss has been recorded.")

        # TODO: Fix this
        elif choice == 5: # Rooms that an employee can enter
            employees_display : list = list(db.employees.find({}))
            names = []
            for index, emp in enumerate(employees_display):
                print(index, ': ', emp['full_name'])
                names.append(emp['full_name'])
            selected_emp_id = db.employees.find_one({
                'full_name': names[int(input('Select a employee > '))]
                })['_id']
            
            rqs = db.room_requests.find({
                'employee': DBRef('employees', selected_emp_id)
            })

            ki_list:list = []
            for rq in rqs:
                ki = db.key_issue.find_one({'room_request', rq['_id']})
                if ki != None:
                    ki_list.append(ki)
            print(ki_list)


            #print(db.room_requests.find({'employee', DBRef('employee', selected_emp_id)}))

            # for index, ki in enumerate(db.key_issue.find({})):
            #     ki_room_request = db.dereference(ki['room_request'])
            #     emp = db.dereference(ki_room_request['employee'])
            #     if (emp['_id'] == selected_emp_id):
            #         ki_key = db.dereference(ki['key'])
            #         hook = db.dereference(ki_key['hook'])

        elif choice == 6:
            print("Choose a key to delete (all key issues associated with that key will also be deleted):")
            keys = list(db.keys.find({}))
            option = 0
            for key in keys:
                hook = db.dereference(key['hook'])
                print(f"Option {option}:  Hook {hook['hook_number']} Key {key['key_number']}")
                option += 1
            response = int(input("Your Choice: "))
            key = keys[response]
            issues = list(db.key_issue.find({'key': DBRef('keys', key['_id'])}))
            for issue in issues:
                issue_ref = DBRef('key_issues', issue['_id'])
                db.key_issue_loss.delete_many({'key_issue': issue_ref})
                db.key_issue_return.delete_many({'key_issue': issue_ref})
                db.key_issue.delete_one({'_id': issue['_id']})
            db.keys.delete_one({'_id': key['_id']})
            print("The key has been deleted.")

        elif choice == 7:
            print("Choose a employee to delete (everything associated with that key will also be deleted):")
            emps = list(db.employees.find({}))
            option = 0
            for emp in emps:
                print(f"Option {option}: {emp['full_name']} ID {emp['_id']}")
                option += 1
            response = int(input("Your Choice: "))
            emp = emps[response]
            requests = list(db.room_requests.find({'employee': DBRef('employees', emp['_id'])}))
            for request in requests:
                issues = list(db.key_issue.find({'room_request': DBRef('room_requests', request['_id'])}))
                for issue in issues:
                    issue_ref = DBRef('key_issues', issue['_id'])
                    db.key_issue_loss.delete_many({'key_issue': issue_ref})
                    db.key_issue_return.delete_many({'key_issue': issue_ref})
                    db.key_issue.delete_one({'_id': issue['_id']})
                db.room_requests.delete_one({'_id': request['_id']})
            db.employees.delete_one({'_id': emp['_id']})
            print("Employee has been successfully deleted.")

        elif choice == 8:
            print("Which hook do you want to add to?")
            hooks = list(db.hooks.find({}))
            option = 0
            for hook in hooks:
                print(f"Option {option}:  Hook {hook['hook_number']}")
                option += 1
            response = int(input("Your Choice: "))
            hook = hooks[response]
            print("Which building?")
            buildings = list(db.buildings.find({}))
            option = 0
            for building in buildings:
                print(f"Option {option}:  {building['name']}")
                option += 1
            response = int(input("Your Choice: "))
            building = buildings[response]

            print("Which room?")
            rooms = list(db.rooms.find({'building': DBRef('buildings', building['_id'])}))
            option = 0
            for room in rooms:
                print(f"Option {option}: {room['room_number']}")
                option += 1
            response = int(input("Your Choice: "))
            room = rooms[response]

            print("Which door?")
            doors = list(db.doors.find({'room': DBRef('rooms', room['_id'])}))
            option = 0
            for door in doors:
                door_name = db.dereference(door['door_name'])
                print(f"Option {option}:{door_name['name']}")
                option += 1
            response = int(input("Your Choice: "))
            door = doors[response]

            new_opening = {
                'hook': DBRef('hooks', hook['_id']),
                'door': DBRef('doors', door['_id'])
            }
            try:
                db.hook_door_opening.insert_one(new_opening)
                print("Door is added to those that can be opened by the hook.")
            except Exception as e:
                print("The hook can already open that door.")

        elif choice == 9:
            print("What room request would you like to update?")
            requests = list(db.room_requests.find({}))
            option = 0
            for request in requests:
                emp = db.dereference(request['employee'])
                room = db.dereference(request['room'])
                building = db.dereference(room['building'])
                print(f"Option {option}: {emp['full_name']} requesting for {building['name']} {room['room_number']}")
                option += 1
            response = int(input("Your Choice: "))
            request = requests[response]

            print("Which employee do you want to move it to?")
            emps = list(db.employees.find({}))
            option = 0
            for emp in emps:
                print(f"Option {option}: {emp['full_name']} ID: {emp['_id']}")
                option += 1
            response = int(input("Your Choice: "))
            emp = emps[response]
            rr_update = {"$set": {
                "employee": DBRef('employees', emp['_id'])
            }}
            db.room_requests.update_one(request, rr_update)
            print(f"The room request has been moved to {emp['full_name']}")

        elif choice == 10:
            print("Which room would you like to oversee?")
            rooms = list(db.rooms.find({}))
            option = 0
            for room in rooms:
                building = db.dereference(room['building'])
                print(f"Option {option}: {building['name']} {room['room_number']}")
                option += 1
            response = int(input("Your Choice: "))
            room = rooms[response]

            requests = list(db.room_requests.find({'room': DBRef('rooms', room['_id'])}))
            emps = []
            for req in requests:
                if db.key_issue.find({'room_request': DBRef('room_requests', req['_id'])}) is not None:
                    emp = db.dereference(req['employee'])
                    if emp not in emps:
                        emps.append(emp)
            print("Here are the employees that can access this room: ")
            for emp in emps:
                print(f"{emp['full_name']}, ID {emp['_id']}")


if __name__ == '__main__':

    # connect
    client: MongoClient = Utilities.startup()

    # initialize
    if 'key_hook' in client.list_database_names():
        client.drop_database('key_hook')
    db = client.key_hook

    IS.insert(db)
    main_menu(db)
    print("Exiting Application ... ")
