#!/usr/bin/python

import argparse
import os
import requests
from typing import Optional
import yaml


REL_SETTINGS_PATH = "./settings.yaml"


def get_settings_path() -> str:
    parent_dir_path = os.path.dirname(__file__)
    return os.path.join(parent_dir_path, REL_SETTINGS_PATH)


def get_config() -> dict:
    if not os.path.exists(get_settings_path()):
        return dict()
    with open(get_settings_path(), 'r') as config_stream:
        config_data = yaml.load(config_stream, Loader=yaml.FullLoader)
        return dict() if config_data is None else config_data


def set_config(chat_id: Optional[int] = None, api_key: Optional[str] = None) -> dict:
    config_data = get_config()
    config_data["chat_id"] = chat_id if chat_id else config_data.get("chat_id", None)
    config_data["token"] = api_key if api_key else config_data.get("token", None)
    with open(get_settings_path(), 'w') as to_update_stream:
        yaml.dump(config_data, to_update_stream, Dumper=yaml.Dumper)
        return config_data


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="A simple usage of the Telegram Bot API.",
                                         allow_abbrev=True)
    default_message = "!"
    arg_parser.add_argument("--chat_id", type=str, help="sets the chat_id in settings")
    arg_parser.add_argument("--token", type=str, help="sets the bot token in settings")
    arg_parser.add_argument("--text", type=str, default=default_message, help="specifies the message to send to chat")
    arg_parser.add_argument("--silence_message", action="store_true", dest="silenced",
                            help=f"silences default '{default_message}' message to chat when no message is specified")
    args = arg_parser.parse_args()
    config = set_config(args.chat_id, args.token)
    if not config or not config.get("chat_id", False) or not config.get("token", False):
        raise Exception("Config file not valid. Use --token and --api_key options to set config values.")
    if not args.silenced:
        data = {"chat_id": config["chat_id"], "text": args.text}
        bot_url = f"https://api.telegram.org/bot{config['token']}/sendMessage"
        response = requests.post(bot_url, data=data)
        print(response)
