"""

This example sends messages to a Telegram chat using the Notifier context manager.

"""

from dotenv import load_dotenv
from telegram_notifier import Notifier

load_dotenv()

with Notifier("Test case") as notifier:
    notifier.send_message("This is a progress update")
