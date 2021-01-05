from datetime import datetime
from .tools import Config, send_message, get_settings_path, escape_specials
import traceback


class Notifier:
    def __init__(self, description: str = "",
                 failed_message_format: str = "`\"{description}\"`\n*_{exc_type}_* - {exc_val}\n" +
                                              "```python\n{exc_tb}```\n ",
                 succeeded_message_format: str = "`\"{description}\"`\nCompleted successfully in {time_duration}",
                 started_message_format: str = "`\"{description}\"` started"):
        self.failed_message_format = failed_message_format
        self.succeeded_message_format = succeeded_message_format
        self.started_message_format = started_message_format
        self.description = description
        self.start_time = None
        self.config = Config(from_file=get_settings_path())

    def __enter__(self):
        self.start_time = datetime.now()
        message = self.started_message_format.format(description=self.description)
        escaped_message = escape_specials(message)
        print(send_message(self.config, escaped_message, parse_mode="MarkdownV2"))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            time_duration = datetime.now() - self.start_time
            message = self.succeeded_message_format.format(time_duration=time_duration,
                                                           process=id(self),
                                                           description=self.description)
            escaped_message = escape_specials(message)
            print(send_message(self.config, escaped_message, parse_mode="MarkdownV2"))
        else:
            formatted_tb = "\n".join(traceback.format_tb(exc_tb)).strip()
            message = self.failed_message_format.format(exc_type=exc_type.__name__,
                                                        exc_val=exc_val,
                                                        exc_tb=formatted_tb,
                                                        process=id(self),
                                                        description=self.description)
            escaped_message = escape_specials(message)
            print(send_message(self.config, escaped_message, parse_mode="MarkdownV2"))
