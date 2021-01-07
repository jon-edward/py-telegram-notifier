import os
from configparser import ConfigParser
from requests import post, Response
from typing import Optional

CONFIG_PATH = "config.ini"


class EmptyMessageError(Exception):
    pass


class InvalidConfigError(Exception):
    pass


def send_message(message: str, **kwargs) -> Optional[Response]:
    if not config_is_valid():
        raise InvalidConfigError("Required config options not defined.")
    config = ConfigParser()
    config.read(CONFIG_PATH)
    if not message:
        raise EmptyMessageError("Sent message cannot be empty.")
    data = {"chat_id": config.get("DEFAULT", "chat_id"),
            "text": escape_specials(message)}
    data.update(kwargs)
    bot_url = f"https://api.telegram.org/bot{config.get('DEFAULT', 'token')}/sendMessage"
    return post(bot_url, data=data)


def escape_specials(to_escape: str) -> str:
    return to_escape.replace("\\", "/").replace("/", "\/").replace("-", "\-").replace(".", "\.")


def set_config_options(chat_id=None, token=None) -> None:
    config = ConfigParser()
    if config_is_valid():
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
