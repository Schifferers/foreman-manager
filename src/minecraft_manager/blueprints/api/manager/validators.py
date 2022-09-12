__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
validators.py
- Validators for API calls
"""


from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema


server_action_schema = {
    '$id': 'http://sweetrpg.com/schemas/server_action.json',
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'server_id': {
            'type': 'string',
        },
        'action': {
            'type': 'string'
        },
    },
    'required': ['server_id', 'action']
}

class ServerActionInput(Inputs):
    json = [JsonSchema(schema=server_action_schema)]
