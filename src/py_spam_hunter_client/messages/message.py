from langdetect import detect, LangDetectException
from langdetect import DetectorFactory

DetectorFactory.seed = 0


class Message:
    """
    Class representing a message with text, language, and an optional ID.
    If language is not provided, it will be detected automatically.
    """
    def __init__(self, text: str, language: str = '', id: str = ''):
        self.__text = text
        self.__language = language if language else self.detect_language(text)
        self.__id = id

    def get_id(self):
        return self.__id

    def get_text(self):
        return self.__text

    def get_language(self):
        return self.__language

    @staticmethod
    def detect_language(text: str):
        try:
            lang = detect(text)
            if lang not in ['en', 'ru']:
                return 'xx'
            return lang
        except LangDetectException:
            return 'xx'
