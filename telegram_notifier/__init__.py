from configparser import ConfigParser
from requests import post, Response
import os
from typing import Optional, Union
import traceback


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")


class EmptyMessageError(Exception):
    pass


class InvalidConfigError(Exception):
    pass


def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config


def send_message(message: str, **kwargs) -> Optional[Response]:
    if not validate_config(get_config()):
        raise InvalidConfigError("Required config options not defined.")
    config = get_config()
    if not message:
        raise EmptyMessageError("Sent message cannot be empty.")
    data = {
        "chat_id": config.get("DEFAULT", "chat_id"),
        "text": escape_specials(message),
    }
    data.update(kwargs)
    bot_url = (
        f"https://api.telegram.org/bot{config.get('DEFAULT', 'token')}/sendMessage"
    )
    return post(bot_url, data=data)


def escape_specials(to_escape: str) -> str:
    return to_escape.replace(".", "\\.").replace("-", "\\-")


def set_config_options(
    chat_id: Optional[Union[str, int]] = None, token: Optional[str] = None
) -> None:
    config = get_config()
    if chat_id is not None:
        config["DEFAULT"]["chat_id"] = str(chat_id)
    if token is not None:
        config["DEFAULT"]["token"] = token
    with open(CONFIG_PATH, "w") as config_stream:
        config.write(config_stream)


def validate_config(config: ConfigParser) -> bool:
    if config.has_option("DEFAULT", "chat_id") and config.has_option(
        "DEFAULT", "token"
    ):
        return bool(config.get("DEFAULT", "chat_id")) and bool(
            config.get("DEFAULT", "token")
        )
    else:
        return False


def process_response(response: Response) -> str:
    if response.ok:
        return "telegram_notifier: Notification sent"
    else:
        return f"telegram_notifier: Error {response.text}"


class Notifier:
    def __init__(
        self,
        description: str = "",
        failed_message_format: str = '`"{description}"`\n*_{exc_type}_* - {exc_val}\n```python\n{exc_tb}```',
        succeeded_message_format: str = '`"{description}"` completed successfully.',
        started_message_format: str = '`"{description}"` started',
        suppress_verbosity: bool = False,
    ):
        self.failed_message_format = failed_message_format
        self.succeeded_message_format = succeeded_message_format
        self.started_message_format = started_message_format
        self.description = description
        self.suppress_verbosity = suppress_verbosity

    def __enter__(self):
        message = self.started_message_format.format(description=self.description)
        response = send_message(message, parse_mode="MarkdownV2")
        if not self.suppress_verbosity:
            print(process_response(response))

    def __exit__(self, exc_type, exc_val, exc_tb):
        exit_message_format = (
            self.succeeded_message_format
            if exc_type is None
            else self.failed_message_format
        )
        formatted_tb = "\n".join(traceback.format_tb(exc_tb)).strip()
        format_data = {
            "exc_type": "" if exc_type is None else exc_type.__name__,
            "exc_val": exc_val,
            "exc_tb": formatted_tb,
            "description": self.description,
        }
        message = exit_message_format.format(**format_data)
        response = send_message(message, parse_mode="MarkdownV2")
        if not self.suppress_verbosity:
            print(process_response(response))
