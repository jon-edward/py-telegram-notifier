"""

This example sends a custom message to a Telegram chat using the Notifier context manager.

"""

import traceback
from types import TracebackType
from typing import Type

from dotenv import load_dotenv
from telegram_notifier import Notifier

load_dotenv()

ROCKET_EMOJI = "🚀"
SMILING_EMOJI = "😊"
SAD_EMOJI = "😢"


def started_message(desc: str) -> str:
    return f"`{desc!r}` started. {ROCKET_EMOJI}"


def succeeded_message(desc: str) -> str:
    return f"`{desc!r}` completed successfully. {SMILING_EMOJI}"


def failed_message(
    desc: str,
    exc_type: Type[BaseException],
    exc_val: BaseException,
    exc_tb: TracebackType,
) -> str:
    formatted_tb = "\n".join(traceback.format_tb(exc_tb)).strip()
    return f"`{desc!r}` failed with {exc_type.__name__} - {exc_val}. {SAD_EMOJI}\n```\n{formatted_tb}```"


notifier = Notifier("Custom task")

notifier.started_message = started_message
notifier.succeeded_message = succeeded_message
notifier.failed_message = failed_message

with notifier:
    notifier.send_message("This is a progress update")
    _ = 1 / 0
