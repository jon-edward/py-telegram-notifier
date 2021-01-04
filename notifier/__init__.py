from datetime import datetime
from config import Config
from __main__ import get_settings_path
import traceback


class Notifier:
    def __init__(self, message_format: str = "*_{}_* - {}\n```{}```"):
        self.start_time = None
        self.config = Config(get_settings_path())

    def set_config(self, entries: dict) -> None:
        self.config.update_entries(entries)

    def save_config(self) -> None:
        self.config.save()

    def __enter__(self):
        self.start_time = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            pass

