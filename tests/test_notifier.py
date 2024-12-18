from telegram_notifier import Notifier
import httpretty
import os
import unittest


TESTING_BOT_TOKEN = "0000000000"
TESTING_CHAT_ID = "0000000000"


def get_text_of_last_request():
    return httpretty.last_request().parsed_body["text"][0]


class NotifierTest(unittest.TestCase):
    def setUp(self) -> None:
        httpretty.enable()

        os.environ["TELEGRAM_TOKEN"] = TESTING_BOT_TOKEN
        os.environ["TELEGRAM_CHAT_ID"] = TESTING_CHAT_ID

        httpretty.register_uri(
            method=httpretty.POST,
            uri=f"https://api.telegram.org/bot{TESTING_BOT_TOKEN}/sendMessage",
            status=200,
        )

    def tearDown(self) -> None:
        os.environ.pop("TELEGRAM_CHAT_ID", None)
        os.environ.pop("TELEGRAM_TOKEN", None)

        httpretty.disable()
        httpretty.reset()

    def test_should_send_error_type_when_failed(self):
        def failed_message_format(_desc, exc_type, _exc_val, _exc_tb):
            return f"{exc_type.__name__}"

        try:
            with Notifier("Test case") as notifier:
                notifier.failed_message = failed_message_format
                _ = 1 / 0
        except ZeroDivisionError:
            pass

        self.assertEqual(get_text_of_last_request(), "ZeroDivisionError")

    def test_should_send_error_value_when_failed(self):
        def failed_message_format(_desc, _exc_type, exc_val, _exc_tb):
            return f"{exc_val}"

        try:
            with Notifier("Test case") as notifier:
                notifier.failed_message = failed_message_format
                _ = 1 / 0
        except ZeroDivisionError:
            pass

        self.assertEqual(get_text_of_last_request(), "division by zero")

    def test_should_send_description_when_failed(self):
        def failed_message_format(desc, _exc_type, _exc_val, _exc_tb):
            return f"{desc}"

        description = "Test case"

        try:
            with Notifier(description) as notifier:
                notifier.failed_message = failed_message_format
                _ = 1 / 0
        except ZeroDivisionError:
            pass

        self.assertEqual(get_text_of_last_request(), description)

    def test_should_pass_exception_outside_of_notifier_block(self):
        with self.assertRaises(ZeroDivisionError):
            with Notifier("Test case"):
                _ = 1 / 0

    def test_should_send_description_when_succeeded(self):
        def succeeded_message_format(desc):
            return f"{desc}"

        description = "Test case"

        with Notifier(description) as notifier:
            notifier.succeeded_message = succeeded_message_format

        self.assertEqual(get_text_of_last_request(), description)

    def test_should_send_description_when_started(self):
        def started_message_format(desc):
            return f"{desc}"

        description = "Test case"

        notifier = Notifier(description)
        notifier.started_message = started_message_format

        with notifier:
            self.assertEqual(get_text_of_last_request(), description)


if __name__ == "__main__":
    unittest.main()
