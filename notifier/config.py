import os
from typing import Optional, Union
import yaml


class Config:
    def __init__(self, from_file: str) -> None:
        self.required_keys = {"chat_id", "token"}
        self.settings_file_path = from_file
        if not os.path.exists(from_file):
            self.entries = dict()
        else:
            with open(from_file, 'r') as config_stream:
                config_data = yaml.load(config_stream, Loader=yaml.FullLoader)
                self.entries = dict() if config_data is None else config_data

    def update_entries(self, entries: dict) -> None:
        self.entries.update(entries)

    def get_entry(self, key) -> Optional[Union[int, str]]:
        return self.entries.get(key, None)

    def save(self) -> None:
        with open(self.settings_file_path, 'w') as to_update_stream:
            yaml.dump(self.entries, to_update_stream, Dumper=yaml.Dumper)

    def validate_keys(self) -> bool:
        return self.required_keys.issubset(set(self.entries.keys()))
