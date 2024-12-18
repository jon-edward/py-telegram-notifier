"""

A context manager for sending messages to a Telegram chat.

"""

import logging
import traceback
from types import TracebackType
from typing import Optional, Type

import requests

from config import Config, get_config


def _default_failed_message(
    desc: str,
    exc_type: Type[BaseException],
    exc_val: BaseException,
    exc_tb: TracebackType,
):
    formatted_tb = "\n".join(traceback.format_tb(exc_tb)).strip()
    prefix = f"`{desc!r}` failed with "
    return f"{prefix if desc else ''}*_{exc_type.__name__}_* - {exc_val}\n```\n{formatted_tb}```"


def _default_succeeded_message(desc: str):
    if desc:
        return f"`{desc!r}` completed successfully."
    return "Completed successfully."


def _default_started_message(desc: str):
    if desc:
        return f"`{desc!r}` started."
    return "Started."


def _escape_reserved(text: str) -> str:
    return text.replace("\\", "\\\\").replace(".", "\\.").replace("-", "\\-")


class Notifier:
    """
    A context manager for sending messages to a Telegram chat.
    """

    desc: str
    config: Config

    failed_message = staticmethod(_default_failed_message)
    """
    A function that takes a description, exception type, exception value, and traceback
    and returns a string to send to the Telegram chat.
    """

    succeeded_message = staticmethod(_default_succeeded_message)
    """
    A function that takes a description and returns a string to send to the Telegram chat.
    """

    started_message = staticmethod(_default_started_message)
    """
    A function that takes a description and returns a string to send to the Telegram chat.
    """

    def __init__(self, desc: str = "", config: Config | None = None):
        """
        :param desc: A description of what the Notifier is doing. Is sent in the message.
        :param config: A Config object. If not provided, uses the default config.
        """
        self.desc = desc
        self.config = config or get_config()

    def send_message(
        self,
        text: str,
        escape_reserved: bool = True,
        parse_mode: str | None = "MarkdownV2",
        **kwargs,
    ) -> requests.Response:
        """
        Sends a message to a Telegram chat.

        :param text: The message to send.
        :param escape_reserved: Whether to escape reserved characters in the message.
        :param parse_mode: The parse mode to use. See the Telegram API docs for more info.
        :param kwargs: Additional data to send. See the Telegram API docs for more info.
        """

        bot_url = f"https://api.telegram.org/bot{self.config.token}/sendMessage"

        data = {
            "chat_id": self.config.chat_id,
            "text": _escape_reserved(text) if escape_reserved else text,
            "parse_mode": parse_mode,
        }
        data.update(kwargs)

        response = requests.post(bot_url, data=data)

        if not response.ok:
            logging.error(f"Failed to send message: %s", response.content)

        return response

    def __enter__(self):
        self.send_message(self.started_message(self.desc))
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):

        if exc_type is not None and exc_val is not None and exc_tb is not None:
            text = self.failed_message(self.desc, exc_type, exc_val, exc_tb)
        else:
            text = self.succeeded_message(self.desc)

        self.send_message(text)
