from typing import Iterable, List

from .messages.checked_message import CheckedMessage
from .messages.message import Message


def build_payload(messages: Iterable[Message], api_key: str) -> dict:
    return {'messages': [message.to_payload() for message in messages], 'api_key': api_key}


def parse_checked_messages(parsed_response: dict) -> List[CheckedMessage]:
    return [
        CheckedMessage(
            message['spam_probability'],
            message.get('id', '')
        )
        for message in parsed_response.get('messages', [])
    ]


def get_error_message(response: dict) -> str:
    try:
        return response['errors'][0]
    except (KeyError, IndexError):
        return response.get('error', 'Unknown error, failed to get a response')
