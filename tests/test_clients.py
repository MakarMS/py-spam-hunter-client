import asyncio
import aiohttp
import pytest
from json import JSONDecodeError

from py_spam_hunter_client.async_spam_hunter_client import AsyncSpamHunterClient
from py_spam_hunter_client.exceptions.check_exception import CheckException
from py_spam_hunter_client.messages.message import Message
from py_spam_hunter_client.sync_spam_hunter_client import SyncSpamHunterClient


class DummyResponse:
    def __init__(self, status_code, json_data=None, json_exc=None):
        self.status_code = status_code
        self._json_data = json_data
        self._json_exc = json_exc

    def json(self):
        if self._json_exc:
            raise self._json_exc
        return self._json_data


class DummyAsyncResponse:
    def __init__(self, status, json_data=None, json_exc=None):
        self.status = status
        self._json_data = json_data
        self._json_exc = json_exc

    async def json(self):
        if self._json_exc:
            raise self._json_exc
        return self._json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummyAsyncSession:
    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def post(self, url, json):
        return self._response


def test_sync_client_success(monkeypatch):
    response = DummyResponse(
        200,
        json_data={"messages": [{"spam_probability": 0.1, "id": "msg-1"}]},
    )

    def fake_post(url, json):
        return response

    monkeypatch.setattr("requests.post", fake_post)
    client = SyncSpamHunterClient("api-key")
    messages = [Message("Hello", ["ctx"], language="en", id="msg-1")]

    checked = client.check(messages)

    assert len(checked) == 1
    assert checked[0].get_spam_probability() == 0.1
    assert checked[0].get_id() == "msg-1"


def test_sync_client_error(monkeypatch):
    response = DummyResponse(400, json_data={"errors": ["bad request"]})

    def fake_post(url, json):
        return response

    monkeypatch.setattr("requests.post", fake_post)
    client = SyncSpamHunterClient("api-key")

    with pytest.raises(CheckException, match="bad request"):
        client.check([Message("Hello", ["ctx"], language="en")])


def test_sync_client_json_error(monkeypatch):
    response = DummyResponse(
        500,
        json_exc=JSONDecodeError("oops", "doc", 0),
    )

    def fake_post(url, json):
        return response

    monkeypatch.setattr("requests.post", fake_post)
    client = SyncSpamHunterClient("api-key")

    with pytest.raises(CheckException, match="Unknown error, failed to get a response"):
        client.check([Message("Hello", ["ctx"], language="en")])


def test_async_client_success(monkeypatch):
    response = DummyAsyncResponse(
        200,
        json_data={"messages": [{"spam_probability": 0.2, "id": "msg-2"}]},
    )
    session = DummyAsyncSession(response)
    monkeypatch.setattr(aiohttp, "ClientSession", lambda: session)

    client = AsyncSpamHunterClient("api-key")
    messages = [Message("Hello", ["ctx"], language="en", id="msg-2")]

    checked = asyncio.run(client.check(messages))

    assert len(checked) == 1
    assert checked[0].get_spam_probability() == 0.2
    assert checked[0].get_id() == "msg-2"


def test_async_client_error(monkeypatch):
    response = DummyAsyncResponse(400, json_data={"error": "forbidden"})
    session = DummyAsyncSession(response)
    monkeypatch.setattr(aiohttp, "ClientSession", lambda: session)

    client = AsyncSpamHunterClient("api-key")

    with pytest.raises(CheckException, match="forbidden"):
        asyncio.run(client.check([Message("Hello", ["ctx"], language="en")]))


def test_async_client_content_type_error(monkeypatch):
    response = DummyAsyncResponse(
        500,
        json_exc=aiohttp.ContentTypeError(request_info=None, history=(), message=""),
    )
    session = DummyAsyncSession(response)
    monkeypatch.setattr(aiohttp, "ClientSession", lambda: session)

    client = AsyncSpamHunterClient("api-key")

    with pytest.raises(CheckException, match="Unknown error, failed to get a response"):
        asyncio.run(client.check([Message("Hello", ["ctx"], language="en")]))
