"""

A module for storing config options.

"""

from dataclasses import dataclass
import os


@dataclass
class Config:
    """
    A class for storing config options.
    """

    chat_id: str
    token: str

    def __repr__(self):
        return f"{self.__class__.__name__}(chat_id={self.chat_id!r}, token=XXXXXX)"

    def __str__(self):
        return f"{self.__class__.__name__}(chat_id={self.chat_id!r}, token=XXXXXX)"


def get_config() -> Config:
    """
    Gets config options from environment variables.
    """

    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    token = os.getenv("TELEGRAM_TOKEN")

    if not chat_id or not token:
        raise ValueError("TELEGRAM_CHAT_ID and TELEGRAM_TOKEN must be set")

    return Config(chat_id, token)
