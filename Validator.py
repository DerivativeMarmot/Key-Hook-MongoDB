class Validator:

    def employees_validator():
        return {
            '$jsonSchema': {
                'bsonType': "object",
                'description': "Valid employees",
                'required': ['id', 'full_name'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'id': {
                        'bsonType': "number",
                        'description': "employee full name.",
                        "minimum": 0,
                        "maximum": 2000
                    },
                    'full_name': {
                        'bsonType': "string",
                        'description': "employee full name.",
                        'maxLength': 200
                    }
                }
            }
    }