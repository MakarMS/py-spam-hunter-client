# 📦 Spam Hunter Client

A Python client for the SpamHunter API to check messages for spam probability.  
This package supports both synchronous and asynchronous usage.

📚 Documentation: [https://spam-hunter.ru/documentation](https://spam-hunter.ru/documentation)

---

## 🚀 Installation

You can install the library via pip:

```bash
pip install py-spam-hunter-client
```

---

## ⚡ Usage

### 🌀 Asynchronous Example

To use the asynchronous version of the API, create an `AsyncSpamHunterClient` instance and call `check` in an async context:

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

---

### 🔁 Synchronous Example

To use the synchronous version of the API, use `SyncSpamHunterClient`:

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

---

## 📘 API Reference

### `check(messages: List[Message]) -> List[CheckedMessage]`

Available in both async and sync clients:

- `AsyncSpamHunterClient.check(messages)` — asynchronous
- `SyncSpamHunterClient.check(messages)` — synchronous

**Parameters:**

- `messages`: A list of [`Message`](#-message-object) instances to be checked.

**Returns:**

- A list of [`CheckedMessage`](#-checkedmessage-object) instances with spam probability results.

**Raises:**

- `CheckException`: Raised if the request fails or the API returns an error.

---

## 📩 Message Object

Represents a message submitted for spam analysis.

**Constructor:**

```python
Message(
    text: str,
    contexts: List[str],
    language: Optional[str] = None,
    id: Optional[str] = None
)
```

**Attributes:**

- `id` (`str`, optional): A custom identifier for the message.
- `text` (`str`): The main content of the message.
- `contexts` (`List[str]`): Previous messages or context (e.g., recent chat history).
- `language` (`str`, optional): Language code:
  - `'en'` — English
  - `'ru'` — Russian
  - `None` — for automatic detection

---

## 🔢 CheckedMessage Object

Represents the result of a spam check returned by the API.

**Attributes:**

- `id` (`str`, optional): The custom ID of the original message.
- `spam_probability` (`float`): A float between `0` and `1` indicating spam likelihood.

**Methods:**

```python
get_spam_probability() -> float
```

Returns the spam probability score for the message.