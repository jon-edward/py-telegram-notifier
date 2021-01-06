import os
from requests import post, Response
from typing import Optional, Union
import yaml

REL_SETTINGS_PATH = "settings.yaml"


class Config:
    def __init__(self) -> None:
        self.required_keys = {"chat_id", "token"}
        self.settings_file_path = get_settings_path()
        if os.path.exists(self.settings_file_path):
            self.entries = dict()
            f = open(get_settings_path(), 'w')
            f.close()
        else:
            with open(self.settings_file_path, 'r') as config_stream:
                config_data = yaml.load(config_stream, Loader=yaml.FullLoader)
                self.entries = dict() if config_data is None else config_data

    def update_entries(self, entries: dict) -> None:
        self.entries.update(entries)

    def get_entry(self, key) -> Optional[Union[int, str]]:
        return self.entries.get(key, None)

    def save(self) -> None:
        if self.settings_file_path is None:
            raise AttributeError("settings file path is not defined")
        with open(self.settings_file_path, 'w') as to_update_stream:
            yaml.dump(self.entries, to_update_stream, Dumper=yaml.Dumper)

    def validate_keys(self) -> bool:
        return self.required_keys.issubset(set(self.entries.keys()))


def get_settings_path() -> str:
    parent_dir_path = os.path.dirname(__file__)
    return os.path.join(parent_dir_path, REL_SETTINGS_PATH)


def send_message(config: Config, message: str, **kwargs) -> Optional[Response]:
    if not message:
        return
    data = {"chat_id": config.get_entry('chat_id'),
            "text": message}
    data.update(kwargs)
    bot_url = f"https://api.telegram.org/bot{config.get_entry('token')}/sendMessage"
    return post(bot_url, data=data)


def escape_specials(to_escape: str) -> str:
    return to_escape.replace("\\", "/").replace("/", "\/").replace("-", "\-").replace(".", "\.")
