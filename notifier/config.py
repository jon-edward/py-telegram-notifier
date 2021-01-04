import os
import yaml


class Config:
    def __init__(self, from_file: str):
        self.settings_file_path = from_file
        if not os.path.exists(from_file):
            self.entries = dict()
        else:
            with open(from_file, 'r') as config_stream:
                config_data = yaml.load(config_stream, Loader=yaml.FullLoader)
                self.entries = dict() if config_data is None else config_data

    def set(self, entries: dict):
        self.entries.update(entries)

    def save(self):
        with open(self.settings_file_path, 'w') as to_update_stream:
            yaml.dump(self.entries, to_update_stream, Dumper=yaml.Dumper)
