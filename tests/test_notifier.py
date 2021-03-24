import telegram_notifier
from telegram_notifier import Notifier, escape_specials, EmptyMessageError
import httpretty
import os
import unittest


TESTING_CHAT_ID, TESTING_BOT_TOKEN = 100, "MyBot"  # Arbitrary
TESTING_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "test_config.ini")


def get_text_of_last_request():
    return httpretty.last_request().parsed_body["text"][0]


class NotifierTest(unittest.TestCase):
    def setUp(self) -> None:
        httpretty.enable()
        telegram_notifier.CONFIG_PATH = TESTING_CONFIG_PATH

        telegram_notifier.set_config_options(
            token=TESTING_BOT_TOKEN,
            chat_id=TESTING_CHAT_ID
        )

        httpretty.register_uri(
            method=httpretty.POST,
            uri=f"https://api.telegram.org/bot{TESTING_BOT_TOKEN}/sendMessage",
            status=200
        )

    def tearDown(self) -> None:
        os.remove(TESTING_CONFIG_PATH)
        httpretty.disable()
        httpretty.reset()

    def test_should_safely_send_message_to_bot_by_escaping_special_characters(self):
        message_to_send = "This contains special characters...-"
        expected_message = "This contains special characters\\.\\.\\.\\-"
        with Notifier("Test case", succeeded_message_format=message_to_send, suppress_verbosity=True):
            # Note: "suppress_verbosity" simply turns off messages printing to the console for clarity in testing.
            pass
        self.assertEqual(get_text_of_last_request(), expected_message)

    def test_should_raise_error_when_sent_message_is_empty(self):
        empty_message_to_send = ""
        with self.assertRaises(EmptyMessageError):
            with Notifier("Test case", succeeded_message_format=empty_message_to_send, suppress_verbosity=True):
                pass

    def test_should_send_error_type_when_failed(self):
        failed_message_format = "{exc_type}"
        try:
            with Notifier("Test case", failed_message_format=failed_message_format, suppress_verbosity=True):
                x = 1 / 0
        except ZeroDivisionError:
            pass
        self.assertEqual(get_text_of_last_request(), "ZeroDivisionError")

    def test_should_send_error_value_when_failed(self):
        failed_message_format = "{exc_val}"
        try:
            with Notifier("Test case", failed_message_format=failed_message_format, suppress_verbosity=True):
                x = 1 / 0
        except ZeroDivisionError:
            pass
        self.assertEqual(get_text_of_last_request(), "division by zero")

    def test_should_send_description_when_failed(self):
        failed_message_format = "{description}"
        description = "Test case"
        try:
            with Notifier(description=description, failed_message_format=failed_message_format, suppress_verbosity=True):
                x = 1 / 0
        except ZeroDivisionError:
            pass
        self.assertEqual(get_text_of_last_request(), escape_specials(description))

    def test_should_pass_exception_outside_of_notifier_block(self):
        with self.assertRaises(ZeroDivisionError):
            with Notifier("Test case", suppress_verbosity=True):
                x = 1 / 0

    def test_should_send_description_when_succeeded(self):
        description = "Test case"
        succeeded_message_format = "{description}"
        with Notifier(description=description, succeeded_message_format=succeeded_message_format, suppress_verbosity=True):
            pass
        self.assertEqual(get_text_of_last_request(), description)


if __name__ == '__main__':
    unittest.main()
