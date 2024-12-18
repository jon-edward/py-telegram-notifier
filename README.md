# py-telegram-notifier

[![PyPI Downloads](https://static.pepy.tech/badge/py-telegram-notifier)](https://pepy.tech/projects/py-telegram-notifier)

A tool using the Telegram Bot API for sending messages to a Telegram chat by
a context manager, function call, or CLI.

## Purpose

The purpose of this module is to provide a simple way to send messages to a Telegram chat using the Telegram Bot API. 
This is especially useful for long-running automation scripts, where the user may not be around to check the logs. 

This is not a wrapper for the Telegram Bot API, but rather a utility for notifying users of enter/exit events with a 
context manager.

## Installation

    pip install py-telegram-notifier

## Requirements

In order for the module to function, you must supply it with a bot
[token](https://core.telegram.org/bots/api#authorizing-your-bot) and a
[chat id](https://core.telegram.org/bots/api#getupdates). Full instructions on creating a bot
can be found [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

## Usage 

Firstly, set up the config for your Notifier. Bot token and chat id are required and must be set as environment 
variables (`TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`, respectively). It's strongly recommended to use a git-ignored `.env` 
file for this purpose, an example file can be found [here](https://github.com/jon-edward/py-telegram-notifier/blob/main/.env.example).

### As a context manager

```python
import dotenv
from telegram_notifier import Notifier

# Load environment variables
dotenv.load_dotenv()

with Notifier("Test case") as notifier:
    # Enter message fired
    notifier.send_message("This is a progress update")
# Exit message fired
```

### As a function call

```python
import dotenv
from telegram_notifier import Notifier

# Load environment variables
dotenv.load_dotenv()

notifier = Notifier()
notifier.send_message("Test message")
# Does not need to be used as a context manager
```

### As a CLI

```bash
TELEGRAM_TOKEN=0000000000 TELEGRAM_CHAT_ID=0000000000 python -m telegram_notifier "Test message"
```

## Notes

This module treats all messages as `MarkdownV2` by default, and escapes known reserved characters. See [`Notifier.send_message()`](https://github.com/jon-edward/py-telegram-notifier/blob/main/telegram_notifier/notifier.py) for more information.


## Disclaimer

The author of this software is not affiliated, associated, authorized, endorsed by, or in any
way officially connected with Telegram or any of its affiliates and is independently owned and
created.
