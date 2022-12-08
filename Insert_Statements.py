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


def insert(db):
    # # connect
    # client: MongoClient = Utilities.startup()

    # # initialize
    # if 'key_hook' in client.list_collection_names():
    #     client.drop_collection('key_hook')
    # db = client.key_hook

    employees = db.employees
    room_requests = db.room_requests
    rooms = db.rooms
    key_issue = db.key_issue
    key_issue_return = db.key_issue_return
    key_issue_loss = db.key_issue_loss
    buildings = db.buildings
    door_names = db.door_names
    doors = db.doors
    hooks = db.hooks
    hook_door_opening = db.hook_door_opening
    keys = db.keys

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

    # employee_v = Validator.employees_validator()
    # room_request_v = Validator.room_requests_validator()
    # k_i_v = Validator.key_issue_validator()
    # k_iss_r_v = Validator.key_issue_return_validator()
    # k_iss_l_v = Validator.key_issue_loss_validator()
    
    # validator
    db.command('collMod', 'employees', validator=Validator.employees_validator())
    db.command('collMod', 'room_requests', validator=Validator.room_requests_validator())
    db.command('collMod', 'key_issue', validator=Validator.key_issue_validator())
    db.command('collMod', 'key_issue_return', validator=Validator.key_issue_return_validator())
    db.command('collMod', 'key_issue_loss', validator=Validator.key_issue_loss_validator())

    building_list = [{'name': 'COB'},
                     {'name': 'PH1'},
                     {'name': 'ECS'},
                     {'name': 'KIN'},
                     {'name': 'PSY'},
                     {'name': 'DESN'}]

    building_results = buildings.insert_many(building_list)

    employee_list = [{'full_name': 'Jimmy Johnson'},
                     {'full_name': 'Micheal Scott'},
                     {'full_name': 'Pam Beasly'},
                     {'full_name': 'Jim Halpert'},
                     {'full_name': 'Ryan Reynolds'},
                     {'full_name': 'Zendeya'}]

    employee_results = employees.insert_many(employee_list)

    room_list = [{'room_number': 30, 'building': DBRef('building', building_results.inserted_ids[0])},
                 {'room_number': 23, 'building': DBRef('building', building_results.inserted_ids[0])},
                 {'room_number': 402, 'building': DBRef('building', building_results.inserted_ids[1])},
                 {'room_number': 105, 'building': DBRef('building', building_results.inserted_ids[5])},
                 {'room_number': 213, 'building': DBRef('building', building_results.inserted_ids[3])},
                 {'room_number': 309, 'building': DBRef('building', building_results.inserted_ids[4])}]

    room_results = rooms.insert_many(room_list)

    door_name_list = [{'name': 'Front'},
                      {'name': 'Back'},
                      {'name': 'East'},
                      {'name': 'West'},
                      {'name': 'North'},
                      {'name': 'South'}]

    door_name_result = door_names.insert_many(door_name_list)

    door_list = [{'door_name': DBRef('door_name', door_name_result.inserted_ids[0]),
                  'room': DBRef('room', room_results.inserted_ids[0])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[1]),
                  'room': DBRef('room', room_results.inserted_ids[0])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[0]),
                  'room': DBRef('room', room_results.inserted_ids[1])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[1]),
                  'room': DBRef('room', room_results.inserted_ids[1])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[2]),
                  'room': DBRef('room', room_results.inserted_ids[2])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[4]),
                  'room': DBRef('room', room_results.inserted_ids[3])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[5]),
                  'room': DBRef('room', room_results.inserted_ids[3])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[0]),
                  'room': DBRef('room', room_results.inserted_ids[4])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[2]),
                  'room': DBRef('room', room_results.inserted_ids[5])},
                 {'door_name': DBRef('door_name', door_name_result.inserted_ids[3]),
                  'room': DBRef('room', room_results.inserted_ids[5])}]

    door_result = doors.insert_many(door_list)

    hook_list = [{'hook_number': 1},
                 {'hook_number': 2},
                 {'hook_number': 3},
                 {'hook_number': 4},
                 {'hook_number': 5},
                 {'hook_number': 6}]

    hook_result = hooks.insert_many(hook_list)

    hook_door_opening_list = [{'hook': DBRef('hook', hook_result.inserted_ids[0]),
                               'door': DBRef('door', door_result.inserted_ids[0])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[0]),
                               'door': DBRef('door', door_result.inserted_ids[1])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[1]),
                               'door': DBRef('door', door_result.inserted_ids[0])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[1]),
                               'door': DBRef('door', door_result.inserted_ids[2])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[1]),
                               'door': DBRef('door', door_result.inserted_ids[3])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[2]),
                               'door': DBRef('door', door_result.inserted_ids[4])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[3]),
                               'door': DBRef('door', door_result.inserted_ids[5])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[3]),
                               'door': DBRef('door', door_result.inserted_ids[6])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[4]),
                               'door': DBRef('door', door_result.inserted_ids[7])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[5]),
                               'door': DBRef('door', door_result.inserted_ids[8])},
                              {'hook': DBRef('hook', hook_result.inserted_ids[5]),
                               'door': DBRef('door', door_result.inserted_ids[9])}]

    hook_door_opening_result = hook_door_opening.insert_many(hook_door_opening_list)

    key_list = [{'key_number': 1, 'hook': DBRef('hook', hook_result.inserted_ids[0])},
                {'key_number': 2, 'hook': DBRef('hook', hook_result.inserted_ids[1])},
                {'key_number': 3, 'hook': DBRef('hook', hook_result.inserted_ids[1])},
                {'key_number': 4, 'hook': DBRef('hook', hook_result.inserted_ids[2])},
                {'key_number': 5, 'hook': DBRef('hook', hook_result.inserted_ids[3])},
                {'key_number': 6, 'hook': DBRef('hook', hook_result.inserted_ids[4])},
                {'key_number': 7, 'hook': DBRef('hook', hook_result.inserted_ids[4])},
                {'key_number': 8, 'hook': DBRef('hook', hook_result.inserted_ids[5])}]

    key_result = keys.insert_many(key_list)

    room_request_list = [{'request_time': datetime.now(),
                          'employee': DBRef('employee', employee_results.inserted_ids[0]),
                          'room': DBRef('room', room_results.inserted_ids[1])},
                         {'request_time': datetime.now(),
                          'employee': DBRef('employee', employee_results.inserted_ids[1]),
                          'room': DBRef('room', room_results.inserted_ids[1])},
                         {'request_time': datetime.now(),
                          'employee': DBRef('employee', employee_results.inserted_ids[2]),
                          'room': DBRef('room', room_results.inserted_ids[4])},
                         {'request_time': datetime.now(),
                          'employee': DBRef('employee', employee_results.inserted_ids[3]),
                          'room': DBRef('room', room_results.inserted_ids[1])},
                         {'request_time': datetime.now(),
                          'employee': DBRef('employee', employee_results.inserted_ids[4]),
                          'room': DBRef('room', room_results.inserted_ids[4])},
                         {'request_time': datetime.now(),
                          'employee': DBRef('employee', employee_results.inserted_ids[3]),
                          'room': DBRef('room', room_results.inserted_ids[5])}]

    room_requests_result = room_requests.insert_many(room_request_list)

    key_issue_list = [{'start_time': datetime.now(),
                       'room_request': DBRef('room_request', room_requests_result.inserted_ids[0]),
                       'key': DBRef('key', key_result.inserted_ids[0])},
                      {'start_time': datetime.now(),
                       'room_request': DBRef('room_request', room_requests_result.inserted_ids[1]),
                       'key': DBRef('key', key_result.inserted_ids[1])},
                      {'start_time': datetime.now(),
                       'room_request': DBRef('room_request', room_requests_result.inserted_ids[2]),
                       'key': DBRef('key', key_result.inserted_ids[5])},
                      {'start_time': datetime.now(),
                       'room_request': DBRef('room_request', room_requests_result.inserted_ids[3]),
                       'key': DBRef('key', key_result.inserted_ids[4])},
                      {'start_time': datetime.now(),
                       'room_request': DBRef('room_request', room_requests_result.inserted_ids[4]),
                       'key': DBRef('key', key_result.inserted_ids[6])},
                      {'start_time': datetime.now(),
                       'room_request': DBRef('room_request', room_requests_result.inserted_ids[5]),
                       'key': DBRef('key', key_result.inserted_ids[7])}]

    key_issue_result = key_issue.insert_many(key_issue_list)
    
    
    from pymongo.errors import BulkWriteError
    try:
        key_issue_return_list = [{'return_date': datetime.now(),
                              'key_issue': DBRef('key_issue', key_issue_result.inserted_ids[0])},
                             {'return_date': datetime.now(),
                              'key_issue': DBRef('key_issue', key_issue_result.inserted_ids[1])}]

        key_issue_return_result = key_issue_return.insert_many(key_issue_return_list)
    except BulkWriteError:
        pass
    

    # key_issue_loss_list = [{'loss_date': datetime.now(),
    #                         'key_issue': DBRef('key_issue', key_issue_result.inserted_ids[2])},
    #                        {'loss_date': datetime.now(),
    #                         'key_issue': DBRef('key_issue', key_issue_result.inserted_ids[3])}]

    # key_issue_loss_result = key_issue_loss.insert_many(key_issue_loss_list)
