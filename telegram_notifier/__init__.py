from datetime import datetime
from .tools import send_message, escape_specials, process_response
import traceback


class Notifier:
    def __init__(self, description: str = "",
                 failed_message_format: str = "`\"{description}\"`\n*_{exc_type}_* - {exc_val}\n```python\n{exc_tb}```",
                 succeeded_message_format: str = "`\"{description}\"` completed successfully.",
                 started_message_format: str = "`\"{description}\"` started"):
        self.failed_message_format = failed_message_format
        self.succeeded_message_format = succeeded_message_format
        self.started_message_format = started_message_format
        self.description = description

    def __enter__(self):
        message = self.started_message_format.format(description=self.description)
        response = send_message(message, parse_mode="MarkdownV2")
        print(process_response(response))

    def __exit__(self, exc_type, exc_val, exc_tb):
        exit_message_format = self.succeeded_message_format if exc_type is None else self.failed_message_format
        formatted_tb = "\n".join(traceback.format_tb(exc_tb)).strip()
        format_data = {
            "exc_type": "" if exc_type is None else exc_type.__name__,
            "exc_val": exc_val,
            "exc_tb": formatted_tb,
            "description": self.description
        }
        message = exit_message_format.format(**format_data)
        response = send_message(message, parse_mode="MarkdownV2")
        print(process_response(response))
