# py-telegram-notifier
A simple CLI written in Python for sending a message to a Telegram chat using the Telegram Bot API.

## usage
Save bot information in settings by using:
    
    py notifier --chat_id XXXX --api_key YYYY --silence_message
    
- ```XXXX```: the [unique identifier](https://core.telegram.org/bots/api#sendmessage) for a target chat. As with the Telegram Bot API, this can be a string to represent the username of a target channel.
- ```YYYY```: the bot [token](https://core.telegram.org/bots/api#making-requests).
- ```--silence_message```: silences the default notification message to the chat.

Send a message to a chat once the settings are saved:

    py notifier --text ZZZZ
    
- ```ZZZZ```: the message to send.
