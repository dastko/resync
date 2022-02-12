import falcon
import ujson
import json

from config import TOKEN_TYPE, SECURITY_TOKEN
from utils.validator import ResponseEncoder

BODY_SUPPORTED_METHODS = ("POST", "PUT", "PATCH", )
NON_BODY_SUPPORTED_METHODS = ("GET", "HEAD", "OPTIONS")


class RequireJSON(object):

    ALLOW_CONTENT_TYPES = [
        falcon.MEDIA_JSON,
        'application/json;charset=UTF-8',
        'application/json',

    ]

    def process_request(self, req, resp):

        if not req.client_accepts_json:

            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.'
            )

        if req.method in BODY_SUPPORTED_METHODS:

            if req.content_type not in RequireJSON.ALLOW_CONTENT_TYPES:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.')


class BodyTransformer(object):

    def process_request(self, req, resp):

        try:

            req.context['queryParams'] = {
                key: value
                for key, value in req.params.items()
            }

            if req.method in BODY_SUPPORTED_METHODS:
                resp_stream = req.stream.read() or b"{}"
                req.context['json'] = ujson.loads(resp_stream.decode('utf-8'))

        except ValueError:
            raise falcon.HTTPBadRequest("Malformed JSON", "Syntax error")

        except UnicodeDecodeError:
            raise falcon.HTTPBadRequest("Invalid encoding", "Could not decode as UTF-8")


class ResponseTransformer(object):

    def process_response(self, req, resp, resource, req_succeeded):

        if getattr(resp, "json", None):
            resp.body = json.dumps(resp.json, cls=ResponseEncoder)


def _token_is_valid(token):

    if token.split(" ")[0] == TOKEN_TYPE:
        token = token.split(" ")[-1]

    if token != SECURITY_TOKEN:
        return False
    return True


class AuthMiddleware(object):

    def process_request(self, req, resp):
        token = req.get_header("Authorization")

        types = ['Token type="Bearer"']

        if token is None:
            description = "Please provide an auth token as part of the request"

            raise falcon.HTTPUnauthorized('Auth token required.', description, types)

        if not _token_is_valid(token):
            description = f"The provided auth token is not valid. Please request a new token and try again."

            raise falcon.HTTPUnauthorized("Authentication required", description, types)
