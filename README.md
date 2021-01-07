# py-telegram-notifier
A simple CLI written in Python for sending a message to a Telegram chat using the Telegram Bot API.

## usage - CLI
Save bot information in settings by using:
    
    notifier --chat_id XXXX --token YYYY
    
- ``XXXX`` the [unique identifier](https://core.telegram.org/bots/api#sendmessage) for a 
  target chat.
- ``YYYY`` the bot [token](https://core.telegram.org/bots/api#making-requests).

Send a message to a chat once the settings are saved:

    notifier --text ZZZZ
    
- ``ZZZZ`` the message to send.

##usage - method calls
Save bot information in settings by 
