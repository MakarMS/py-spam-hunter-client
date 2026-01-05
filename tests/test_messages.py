import pytest

from py_spam_hunter_client.messages.checked_message import CheckedMessage
from py_spam_hunter_client.messages import message as message_module
from py_spam_hunter_client.messages.message import Message


def test_message_detects_language():
    message = Message("Hello there", ["greeting"])
    assert message.get_language() == "en"


def test_message_uses_provided_language():
    message = Message("Hello there", ["greeting"], language="ru")
    assert message.get_language() == "ru"


def test_message_detects_russian_language(monkeypatch):
    monkeypatch.setattr(message_module, "detect", lambda text: "ru")
    message = Message("Привет мир", ["greeting"])
    assert message.get_language() == "ru"


def test_message_maps_unknown_language_to_xx(monkeypatch):
    monkeypatch.setattr(message_module, "detect", lambda text: "fr")
    message = Message("Bonjour", ["greeting"])
    assert message.get_language() == "xx"


def test_message_handles_empty_text():
    message = Message("", ["empty"])
    assert message.get_language() == "xx"


def test_message_payload_matches_fields():
    message = Message("Hello", ["ctx"], language="en", id="msg-1")
    assert message.to_payload() == {
        "id": "msg-1",
        "message": "Hello",
        "contexts": ["ctx"],
        "language": "en",
    }


def test_checked_message_getters():
    checked = CheckedMessage(0.42, id="check-1")
    assert checked.get_id() == "check-1"
    assert checked.get_spam_probability() == 0.42
