from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

setting_schema = {
    "type": "object",
    "properties": {
        "project":{
            "type": "string"
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "apiKey":{
            "type": "string"
        },
        "productionKey": {
            "type": "string"
        },
        "developKey": {
            "type": "string"
        },
        "inProduction": {
            "type": "boolean"
        },
        "subProductId": {
            "type": "string"
        },
        "subProductDevId": {
            "type": "string"
        },
        "subProductName": {
            "type": "string"
        },
        "subPlanDevId": {
            "type": "string"
        },
        "subPlanAmount": {
            "type": "number"
        },
        "subPlanCurrency": {
            "type": "string"
        },
        "subPlanInterval": {
            "type": "string"
        },
        "successfulWebhook": {
            "type": "string"
        },
        "cancelWebhook": {
            "type": "string"
        }
    },
    "required": ["project", "email", "productionKey", "developKey", "inProduction", 
                 "subProductName", "subPlanAmount", "subPlanCurrency", "subPlanInterval", "successfulWebhook", "cancelWebhook"],
    "additionalProperties": False
}


def validate_stting(data):
    try:
        validate(data, setting_schema)
    except ValidationError as e:
        return {'ok': False, 'data': e}
    except SchemaError as e:
        return {'ok': False, 'data': e}
    return {'ok': True, 'data': data}
