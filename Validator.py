
class Validator:

    def employees_validator():
        return {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Valid employees",
                # 'required': ['id', 'full_name'],
                'required': ['full_name'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    # 'id': {
                    #     'bsonType': "number",
                    #     'description': "employee full name.",
                    #     "minimum": 0,
                    #     "maximum": 2000
                    # },
                    'full_name': {
                        'bsonType': "string",
                        'description': "employee full name.",
                        'maxLength': 200
                    }
                }
            }
        }
    
    def room_requests_validator():
        return {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Valid room reqeusts",
                # 'required': ['request_id', 'request_time', 'employee_id', 'building_name', 'room_number'],
                # 'required': ['request_time', 'employee', 'room'],
                'required': ['request_time', 'employee', 'room'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    # 'request_id': {
                    #     'bsonType': "number",
                    #     'description': "request id.",
                    #     "minimum": 0
                    # },
                    'request_time': {
                        'bsonType': "date",
                        'description': "request time."
                    },
                    'employee': {
                        'bsonType': "object",
                        'description': "employee reference."
                    },
                    'room': {
                        'bsonType': "object",
                        'description': "room reference."
                    }
                }
            }
        }
    
    def key_issue_validator():
        return {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Valid key issue",
                'required': ['start_time', 'room_request', 'key'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'start_time': {
                        'bsonType': "date",
                        'description': "start time."
                    },
                    'room_request': {
                        'bsonType': "object",
                        'description': "room request reference."
                    },
                    'key': {
                        'bsonType': "object",
                        'description': "key reference."
                    }
                }
            }
        }
    
    def key_issue_return_validator():
        return {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Valid key issue",
                'required': ['loss_date', 'key_issue'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'loss_date': {
                        'bsonType': "date",
                        'description': "loss date."
                    },
                    'key_issue': {
                        'bsonType': "object",
                        'description': "key issue reference."
                    }
                }
            }
        }
    
    def key_issue_loss_validator():
        return {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Valid key issue",
                'required': ['return_date', 'key_issue'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'return_date': {
                        'bsonType': "date",
                        'description': "return date."
                    },
                    'key_issue': {
                        'bsonType': "object",
                        'description': "key issue reference."
                    }
                }
            }
        }

    def buildings_validator():
        return {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "Valid Building",
                    'required': ["name"],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {},
                        'name': {
                            'bsonType': "string",
                            'description': "building name"
                        }
                    }
                }
            }
        }


    def rooms_validator():
        return {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "Valid Room",
                    'required': ['room_number', 'building'],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {},
                        'room_number': {
                            'bsonType': "int",
                            'description': 'room number'
                        },
                        'building': {
                            'bsonType': "object",
                            'description': "building reference"
                        }
                    }
                }
            }
        }

    def door_names_validator():
        return {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "Valid Door Name",
                    'required': ['name'],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {},
                        'name': {
                            'bsonType': "string",
                            'description': 'door name'
                        }
                    }
                }
            }
        }

    def doors_validator():
        return {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "Valid Door",
                    'required': ['building', 'room', 'door_name'],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {}
                        'room': {
                            'bsonType': "object",
                            'description': "room reference"
                        },
                        'door_name': {
                            'bsonType': "object",
                            'description': "door_name reference"
                        }
                    }
                }
            }
        }

    def hooks_validator():
        return {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "Valid Hook",
                    'required': ['hook_number'],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {},
                        'hook_number': {
                            'bsonType': "int",
                            'description': 'hook number'
                        }
                    }
                }
            }
        }

    def hook_door_opening_validator():
        return {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "Valid Hook",
                    'required': ['hook_number'],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {},
                        'hook': {
                            'bsonType': "object",
                            'description': 'hook reference'
                        },
                        'door': {
                            'bsontype': 'object',
                            'description': 'door reference'
                        }
                    }
                }
            }
        }



    def keys_validator():
        return {
            'validator': {
                '$jsonSchema': {
                    'bsonType': "object",
                    'description': "Valid Room",
                    'required': ['room_number', 'building'],
                    'additionalProperties': False,
                    'properties': {
                        '_id': {},
                        'key_number': {
                            'bsonType': "int",
                            'description': 'key number'
                        },
                        'hook': {
                            'bsonType': "object",
                            'description': "building reference"
                        }
                    }
                }
            }
        }


