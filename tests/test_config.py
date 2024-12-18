from telegram_notifier import get_config, Notifier
import os
import unittest


TESTING_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "test_config.ini")

TESTING_BOT_TOKEN = "0000000000"
TESTING_CHAT_ID = "0000000000"


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.pop("TELEGRAM_CHAT_ID", None)
        os.environ.pop("TELEGRAM_TOKEN", None)

    def tearDown(self) -> None:
        os.environ.pop("TELEGRAM_CHAT_ID", None)
        os.environ.pop("TELEGRAM_TOKEN", None)

    def test_get_successful_config(self):
        os.environ["TELEGRAM_CHAT_ID"] = TESTING_CHAT_ID
        os.environ["TELEGRAM_TOKEN"] = TESTING_BOT_TOKEN

        config = get_config()

        self.assertEqual(config.chat_id, TESTING_CHAT_ID)
        self.assertEqual(config.token, TESTING_BOT_TOKEN)

    def test_get_incomplete_config(self):
        # Missing TELEGRAM_CHAT_ID and TELEGRAM_TOKEN
        with self.assertRaises(ValueError):
            get_config()

        # Missing TELEGRAM_CHAT_ID
        os.environ["TELEGRAM_TOKEN"] = TESTING_BOT_TOKEN
        with self.assertRaises(ValueError):
            get_config()
        os.environ.pop("TELEGRAM_TOKEN", None)

        # Missing TELEGRAM_TOKEN
        os.environ["TELEGRAM_CHAT_ID"] = TESTING_CHAT_ID
        with self.assertRaises(ValueError):
            get_config()

    def test_should_get_config_from_env_on_init(self):
        os.environ["TELEGRAM_CHAT_ID"] = TESTING_CHAT_ID
        os.environ["TELEGRAM_TOKEN"] = TESTING_BOT_TOKEN

        notifier = Notifier()

        config = notifier.config

        self.assertEqual(config.chat_id, TESTING_CHAT_ID)
        self.assertEqual(config.token, TESTING_BOT_TOKEN)


if __name__ == "__main__":
    unittest.main()
