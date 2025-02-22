import aiohttp
from typing import List

from src.py_spam_hunter_client.exceptions.check_exception import CheckException
from src.py_spam_hunter_client.messages.checked_message import CheckedMessage
from src.py_spam_hunter_client.messages.message import Message


class AsyncSpamHunterClient:
    BASE_URL = 'https://backend.spam-hunter.ru/api/v1/check'

    def __init__(self, api_key: str):
        self.__api_key = api_key

    async def check(self, messages: List[Message]) -> List[CheckedMessage]:
        """
        Checks a list of messages for spam probability.
        :param messages: A list of Message objects to be checked.
        :return: A list of CheckedMessage objects with spam probability and IDs.
        :raises CheckException: If the request fails or the API returns an error.
        """
        data = {'messages': [], 'api_key': self.__api_key}

        for message in messages:
            data['messages'].append(
                {
                    'id': message.get_id(),
                    'message': message.get_text(),
                    'language': message.get_language()
                }
            )

        async with aiohttp.ClientSession() as session:
            async with session.post(self.BASE_URL, json=data) as response:
                try:
                    parsed_response = await response.json()
                except aiohttp.ContentTypeError:
                    raise CheckException('Unknown error, failed to get a response')

                if response.status == 200:
                    checked_messages = [
                        CheckedMessage(
                            message['spam_probability'],
                            message.get('id', '')
                        )
                        for message in parsed_response.get('messages', [])
                    ]
                    return checked_messages
                else:
                    raise CheckException(self.__get_error_message(parsed_response))

    @staticmethod
    def __get_error_message(response: dict) -> str:
        try:
            return response['errors'][0]
        except (KeyError, IndexError):
            return response.get('error', 'Unknown error, failed to get a response')
