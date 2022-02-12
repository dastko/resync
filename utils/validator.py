import json
import falcon
from functools import wraps
from jsonschema import validate, ValidationError
from datetime import datetime


class ResponseEncoder(json.JSONEncoder):

    def default(self, o):

        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def validate_request(json_schema, field_to_validate="json"):

    def _validate(f):

        @wraps(f)
        def _wrap(*args, **kwargs):
            req_obj = [
                arg
                for arg in args if isinstance(arg, falcon.Request)
            ]
            resp_obj = [
                arg
                for arg in args if isinstance(arg, falcon.Response)
            ]

            if len(req_obj) and len(resp_obj):
                req_obj = req_obj[0]
                resp_obj = resp_obj[0]
                req_json = req_obj.context.get(field_to_validate, None)

                if not req_json:
                    resp_obj.status = falcon.HTTP_400
                    resp_obj.json = {
                        "message": "Invalid request data.",
                        "additionalMessage": {
                            "reason": "Request data is not provided."
                        }
                    }

                    return

                try:
                    validate(req_json, json_schema)

                    return f(*args, **kwargs)
                except ValidationError as vexc:
                    resp_obj.status = falcon.HTTP_400
                    resp_obj.json = {
                        "message": "Invalid request data.",
                        "additionalMessage": {
                            "reason": vexc.message
                        }
                    }
            else:
                return f(*args, **kwargs)

        return _wrap

    return _validate


WORD_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "word": {
            "type": "string"
        },
        "synonyms": {
            "type": "array"
        }
    },
    "required": [
        "word",
        "synonyms"
    ]
}
