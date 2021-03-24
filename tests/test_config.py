import telegram_notifier
from telegram_notifier import set_config_options, Notifier, get_config, InvalidConfigError
import os
import unittest


TESTING_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "test_config.ini")


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        telegram_notifier.CONFIG_PATH = TESTING_CONFIG_PATH

    def tearDown(self) -> None:
        if os.path.exists(TESTING_CONFIG_PATH):
            os.remove(TESTING_CONFIG_PATH)

    def test_should_create_config_file_when_none_exists(self):
        self.assertFalse(os.path.exists(TESTING_CONFIG_PATH))
        set_config_options()
        self.assertTrue(os.path.exists(TESTING_CONFIG_PATH))

    def test_should_safely_get_empty_config_when_none_exists(self):
        self.assertFalse(os.path.exists(TESTING_CONFIG_PATH))
        config = get_config()
        self.assertTrue(config)
        self.assertFalse(config.has_option("DEFAULT", "chat_id"))
        self.assertFalse(config.has_option("DEFAULT", "token"))

    def test_should_set_options_of_config(self):
        # Potential gotcha: Because of how the config is stored, set_config_options will accept an integer for chat_id,
        # but it will save and reload it as a string.
        chat_id = 100
        token = "MyBot"
        set_config_options(chat_id=chat_id, token=token)
        self.assertEqual(get_config()["DEFAULT"]["chat_id"], str(chat_id))
        self.assertEqual(get_config()["DEFAULT"]["token"], token)

    def test_should_set_options_of_config_separately(self):
        chat_id = 100
        token = "MyBot"
        set_config_options(chat_id=chat_id)
        set_config_options(token=token)
        self.assertEqual(get_config()["DEFAULT"]["chat_id"], str(chat_id))
        self.assertEqual(get_config()["DEFAULT"]["token"], token)

    def test_should_raise_an_error_when_notifier_is_initialized_with_an_invalid_config(self):
        chat_id = 100
        token = "MyBot"
        self.assertFalse(os.path.exists(TESTING_CONFIG_PATH))

        with self.assertRaises(InvalidConfigError):
            with Notifier("Test case", suppress_verbosity=True):
                pass

        set_config_options(chat_id=chat_id)

        with self.assertRaises(InvalidConfigError):
            with Notifier("Test case", suppress_verbosity=True):
                pass

        set_config_options(token=token)
        # Both necessary options are set at this point.

        with Notifier("Test case", suppress_verbosity=True):
            pass


if __name__ == '__main__':
    unittest.main()
