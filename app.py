import falcon

from api.rest import SynonymResources
from config import LOGGER
from middleware import RequireJSON, BodyTransformer, ResponseTransformer, AuthMiddleware

LOGGER.debug("Initializing Context...")


def handle_error(ex, _, resp, params):

    LOGGER.debug(params)
    LOGGER.exception(ex)

    if isinstance(ex, falcon.HTTPError):
        resp.status = ex.status
        resp.json = {
            "msg": ex.status,
            "additionalMessage": {
                "code": ex.code,
                "title": ex.title
            }
        }
    else:
        resp.status = falcon.HTTP_500
        resp.json = {
            "msg": "Un-excepted error occur.",
            "additionalMessage": {
                "reason": str(ex)
            }
        }


app = falcon.API(
    middleware=[
        AuthMiddleware(),
        RequireJSON(),
        BodyTransformer(),
        ResponseTransformer()
    ]
)

app.add_route('/synonym', SynonymResources())

app.add_error_handler(Exception, handle_error)
