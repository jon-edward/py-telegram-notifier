# py-telegram-notifier
A simple utilization of the Telegram Bot API for sending messages to a Telegram chat by means of 
a context manager, method calls, or a CLI.

## Installation
    pip install py-telegram-notifier

## Requirements
In order for the module to function, you must supply it with a bot 
[token](https://core.telegram.org/bots/api#authorizing-your-bot), and a 
[chat id](https://core.telegram.org/bots/api#sendmessage). Full instructions on creating a bot 
can be found [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

## Usage as context manager
Firstly, set up the config for your Notifier. This only has to be done once, assuming you are 
sending messages from the same bot to the same chat every time.
```python
from telegram_notifier.tools import set_config_options

chat_id = 0000000000 # Your chat id
token = "0000000000" # Your bot token

set_config_options(chat_id=chat_id, token=token)
```
Then, you may use a Notifier as a context manager that will notify you of the type of exit 
that was encountered, including whether it finished with or without an error.
```python
from telegram_notifier import Notifier

with Notifier("This is a task."):
    # Code that takes a long time.
    pass
```

## Usage as CLI
Save bot information in settings by using:
    
    telegram_notifier --chat_id XXXX --token YYYY
    
- ``XXXX`` the unique identifier for a target chat (chat id).
- ``YYYY`` the bot token.

Send a message to a chat once the settings are saved:

    telegram_notifier --message ZZZZ
    
- ``ZZZZ`` the message to send.

## Disclaimer
The author of this software is not affiliated, associated, authorized, endorsed by, or in any 
way officially connected with Telegram or any of its affiliates and is independently owned and 
created. 