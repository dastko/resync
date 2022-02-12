import falcon
from config import LOGGER
from service.synonym import Synonym
from utils.validator import validate_request, WORD_POST_SCHEMA


class SynonymResources(object):

    def __init__(self):
        self.db = Synonym()

    def on_get(self, req, resp):
        query_params = req.context['queryParams']

        try:
            word = query_params.get('word', None)
            resp.json = self.db.get(word)
        except (ValueError, Exception) as exc:
            resp.status = falcon.HTTP_404
            resp.json = {
                "message": "This word is not available, please consider adding one.",
                "additionalMessage": {
                    "reason": str(exc)
                }
            }

    @validate_request(WORD_POST_SCHEMA, "json")
    def on_post(self, req, resp):
        data = req.context["json"]
        try:
            word = data["word"]
            synonyms = data["synonyms"]
            if word:
                if self.db.exist(word):
                    resp.json = {"message": f"Word {word} already exists, please use PUT method to update synonyms!"}
                    return resp.json
            result = self.db.add(word, synonyms)
            resp.json = {"message": f"Word {result} successfully added!"}
        except (ValueError, Exception) as exc:
            resp.status = falcon.HTTP_500
            resp.json = {
                "message": "This word cannot be added at the moment",
                "additionalMessage": {
                    "reason": str(exc)
                }
            }

    @validate_request(WORD_POST_SCHEMA, "json")
    def on_put(self, req, resp):
        data = req.context["json"]
        try:
            word = data["word"]
            synonyms = data["synonyms"]
            if word:
                if not self.db.exist(word):
                    resp.json = {"message": f"Word {word} is not found! Use POST method to create new word"}
                    resp.status = falcon.HTTP_404
                    return
            result = self.db.add(word, synonyms)
            resp.json = {"message": f"Word {result} successfully added!"}
        except (ValueError, Exception) as exc:
            resp.status = falcon.HTTP_500
            resp.json = {
                "message": "This word cannot be added at the moment",
                "additionalMessage": {
                    "reason": str(exc)
                }
            }

    def on_delete(self, req, resp):
        query_params = req.context['queryParams']
        try:
            word = query_params.get('word', None)
            resp.json = self.db.delete(word)
        except (ValueError, Exception) as exc:
            LOGGER.exception(f"Word is not deleted! {exc}")
            resp.status = falcon.HTTP_500
            resp.json = {
                "message": "Word cannot be removed.",
                "additionalMessage": {
                    "reason": str(exc)
                }
            }
