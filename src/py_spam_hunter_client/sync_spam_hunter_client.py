from json import JSONDecodeError

import requests
from typing import List

from .client_utils import build_payload, get_error_message, parse_checked_messages
from .exceptions.check_exception import CheckException
from .messages.checked_message import CheckedMessage
from .messages.message import Message


class SyncSpamHunterClient:
    BASE_URL = 'https://backend.spam-hunter.ru/api/v1/check'

    def __init__(self, api_key: str):
        self.__api_key = api_key

    def check(self, messages: List[Message]) -> List[CheckedMessage]:
        """
        Checks a list of messages for spam probability
        :param messages: A list of Message objects to be checked.
        :return: A list of CheckedMessage objects with spam probability and IDs.
        :raises CheckException: If the request fails or the API returns an error.
        """
        data = build_payload(messages, self.__api_key)

        response = requests.post(self.BASE_URL, json=data)

        try:
            parsed_response = response.json()
        except JSONDecodeError:
            raise CheckException('Unknown error, failed to get a response')

        if response.status_code == 200:
            return parse_checked_messages(parsed_response)
        raise CheckException(get_error_message(parsed_response))
