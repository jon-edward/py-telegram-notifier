"""

A tool using the Telegram Bot API for sending messages to a Telegram chat by a context manager, function call, or CLI.

"""

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent))

from notifier import Notifier
from config import get_config, Config

__all__ = ["Notifier", "get_config", "Config"]
