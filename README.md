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
      Message('Кто хочет заработать? В ЛС!', 'ru'),
      Message('Кто хочет заработать? В ЛС!')
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
    Message('Кто хочет заработать? В ЛС!', 'ru'),
    Message('Кто хочет заработать? В ЛС!')
  ]
)

for checked_message in checked_messages:
  print(checked_message.get_spam_probability())
```
    

### Methods
`AsyncSpamHunterClient.check(messages: List[Message]) -> List[CheckedMessage]`<br>`SyncSpamHunterClient.check(messages: List[Message]) -> List[CheckedMessage]`

**CheckException** if the request fails or if the API returns an error.

### Message Object

- **id** (`str`): (Optional) A custom ID for the message.
- **text** (`str`): The content of the message.
- **language** (`str`): The language of the message. It can be either:
  - `'ru'` (Russian)
  - `'en'` (English)
  - Left empty for auto-detection.

### CheckedMessage Object

- **id** (`str`): (Optional) The custom ID of the checked message.
- **spam_probability** (`float`): The spam probability of the message, a value between 0 and 1.

