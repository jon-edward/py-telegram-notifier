import os
from configparser import ConfigParser
from requests import post, Response
from typing import Optional

CONFIG_PATH = "config.ini"


def send_message(message: str, **kwargs) -> Optional[Response]:
    config = ConfigParser()
    config.read(CONFIG_PATH)
    if not message:
        return
    data = {"chat_id": config.get("DEFAULT", "chat_id"),
            "text": escape_specials(message)}
    data.update(kwargs)
    bot_url = f"https://api.telegram.org/bot{config.get('DEFAULT', 'token')}/sendMessage"
    return post(bot_url, data=data)


def escape_specials(to_escape: str) -> str:
    return to_escape.replace("\\", "/").replace("/", "\/").replace("-", "\-").replace(".", "\.")


def update_config(chat_id=None, token=None) -> None:
    """Updates config globally. ignores chat_id and token if None"""
    config = ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
    else:
        config["DEFAULT"] = {"chat_id": "", "token": ""}
    if chat_id is not None:
        config["DEFAULT"]["chat_id"] = chat_id
    if token is not None:
        config["DEFAULT"]["token"] = token
    with open(CONFIG_PATH, 'w') as config_stream:
        config.write(config_stream)


def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config


def config_is_valid() -> bool:
    config = get_config()
    return config.has_option("DEFAULT", "chat_id") and config.has_option("DEFAULT", "token")
