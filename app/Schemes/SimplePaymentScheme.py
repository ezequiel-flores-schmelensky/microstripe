# coding=utf-8
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

simple_payment_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "stripeToken": {
            "type": "string"
        },
        "amount": {
            "type": "number"
        },
        "currency": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    },
    "required": ["email", "stripeToken", "amount", "currency", "description"],
    "additionalProperties": False
}


def validate_simple_payment(data):
    try:
        validate(data, curses_payment_schema)
    except ValidationError as e:
        return {'ok': False, 'data': e}
    except SchemaError as e:
        return {'ok': False, 'data': e}
    return {'ok': True, 'data': data}
