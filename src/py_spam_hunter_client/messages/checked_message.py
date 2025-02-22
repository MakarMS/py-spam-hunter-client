class CheckedMessage:
    def __init__(self, spam_probability: float, id: str = ''):
        self.__id = id
        self.__spam_probability = spam_probability

    def get_id(self):
        return self.__id

    def get_spam_probability(self):
        return self.__spam_probability
