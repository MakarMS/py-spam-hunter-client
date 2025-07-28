# Spam Hunter Client

A Python client for SpamHunter API to check messages for spam probability.<br>This package supports both synchronous and asynchronous usage.

Documentation: https://spam-hunter.ru/documentation

## Installation

You can install the library via pip:

`pip install py-spam-hunter-client`

## Usage

### Asynchronous Example

To use the asynchronous version of the API, you can create an `AsyncSpamHunterClient` instance and call `check` in an asynchronous context. Below is an example of how to use it with `asyncio`:

```python
import asyncio
from py_spam_hunter_client import AsyncSpamHunterClient, Message


async def check_messages():
  spam_hunter = AsyncSpamHunterClient('Your API key')

  checked_messages = await spam_hunter.check(
    [
      Message('Who wants to make money? PM ME!', ['Hey, everybody.', 'Did you like the movie?'], 'en'),
      Message('Who wants to make money? PM ME!', ['Hey, everybody.', 'Did you like the movie?']),
      Message('Кто хочет заработать? В ЛС!', ['Привет всем.', 'Тебе понравился фильм?'], 'ru'),
      Message('Кто хочет заработать? В ЛС!', ['Привет всем.', 'Тебе понравился фильм?'])
    ]
  )

  for checked_message in checked_messages:
    print(checked_message.get_spam_probability())


asyncio.run(check_messages())
```

### Synchronous Example
To use the synchronous version of the API, you can use `SyncSpamHunterClient`. Here's an example of how to use it in a normal Python function:

```python
from py_spam_hunter_client import SyncSpamHunterClient, Message

spam_hunter = SyncSpamHunterClient('Your API key')

checked_messages = spam_hunter.check(
  [
      Message('Who wants to make money? PM ME!', ['Hey, everybody.', 'Did you like the movie?'], 'en'),
      Message('Who wants to make money? PM ME!', ['Hey, everybody.', 'Did you like the movie?']),
      Message('Кто хочет заработать? В ЛС!', ['Привет всем.', 'Тебе понравился фильм?'], 'ru'),
      Message('Кто хочет заработать? В ЛС!', ['Привет всем.', 'Тебе понравился фильм?'])
  ]
)

for checked_message in checked_messages:
  print(checked_message.get_spam_probability())
```

### 📘 API Reference

#### `check(messages: List[Message]) -> List[CheckedMessage]`

The `check` method is available in both asynchronous and synchronous clients:

* `AsyncSpamHunterClient.check(messages)` — asynchronous call
* `SyncSpamHunterClient.check(messages)` — synchronous call

**Parameters:**

* `messages`: A list of [`Message`](#message-object) instances to be checked.

**Returns:**

* A list of [`CheckedMessage`](#checkedmessage-object) instances with spam probability results.

**Exceptions:**

* `CheckException` — Raised if the request fails or the API returns an error.

---

### 📩 Message Object

The `Message` class represents a message to be checked by the API.

**Constructor Parameters:**

```python
Message(
    text: str,
    contexts: List[str],
    language: Optional[str] = None,
    id: Optional[str] = None
)
```

**Fields:**

* `id` (`str`, optional): A custom identifier for the message.
* `text` (`str`): The main content of the message.
* `contexts` (`List[str]`): Previous messages or context for the message (e.g., recent chat history).
* `language` (`str`, optional): Language code — can be:

  * `'en'` for English
  * `'ru'` for Russian
  * or left empty to enable automatic language detection

---

### 🔢 CheckedMessage Object

The `CheckedMessage` class represents the result of a spam check.

**Fields:**

* `id` (`str`, optional): The custom ID of the original `Message`, if provided.
* `spam_probability` (`float`): The spam probability score — a float between `0` (not spam) and `1` (definitely spam).

**Methods:**

* `get_spam_probability() -> float`: Returns the spam probability score for the message.