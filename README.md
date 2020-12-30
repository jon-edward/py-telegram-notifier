# py-telegram-notifier
A simple CLI written in Python for sending a message to a Telegram chat using the Telegram Bot API.

## usage
Save bot information in settings by using:
    
    py notifier --chat_id XXXX --token YYYY
    
- ```XXXX```: the [unique identifier](https://core.telegram.org/bots/api#sendmessage) for a target chat.
- ```YYYY```: the bot [token](https://core.telegram.org/bots/api#making-requests).

Send a message to a chat once the settings are saved:

    py notifier --text ZZZZ
    
- ```ZZZZ```: the message to send.
