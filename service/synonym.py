from config import LOGGER, DATABASE
import requests
from bs4 import BeautifulSoup


class Synonym(object):

    def __init__(self, direction=False):
        self._graph = DATABASE
        self.direction = direction

    def add(self, word: str, synonyms: [str]):
        if word and len(synonyms) > 0:
            if not isinstance(word, str):
                raise ValueError(f"Word should be string")

            LOGGER.info(f"Adding new word {word} and connected synonyms{synonyms}")

            for synonym in synonyms:
                if isinstance(synonym, str):
                    self._graph.add(word, synonym)
                else:
                    LOGGER.error(f"Synonym {synonym} is not string!")
            return word
        else:
            raise ValueError(f"Word cannot be empty at least 1 synonym should be added!")

    def exist(self, word):
        if word:
            return self._graph.exist(word)
        else:
            raise ValueError(f"Word cannot be empty!")

    def delete(self, words: [str]):
        if len(words) > 0:
            for word in words:
                if isinstance(word, str):
                    self._graph.remove(word)
                else:
                    LOGGER.error(f"Word {word} is not string!")
        else:
            raise ValueError(f"At least 1 word should be added!")

    def get(self, word: str):
        if word:
            result = self._graph.find(word)
            if result:
                result.remove(word)
            else:
                suggestions = self._find_suggestions(word)
                if suggestions:
                    return {"word": word, "suggestedSynonyms": suggestions}
                else:
                    raise ValueError(f"Word is not found and suggestions are not available.")
            return {"word": word, "synonyms": list(result)}
        else:
            raise ValueError(f"Word should be provided!")

    @staticmethod
    def _find_suggestions(word):
        try:
            response = requests.get(f'https://www.thesaurus.com/browse/{word}')
            soup = BeautifulSoup(response.text, 'html.parser')
            soup.find('section', {'id': 'meanings'})
            suggestions = [span.text.strip(" ") for span in soup.findAll('a', {
                'class': 'css-1kg1yv8 eh475bn0'})]
            if suggestions:
                return suggestions
            return []
        except Exception as exc:
            LOGGER.debug(f"Suggestions for word {word} not found. Stacktrace {exc}")
            return []
