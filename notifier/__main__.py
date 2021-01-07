#!/usr/bin/python

import argparse
from .tools import send_message, update_config, get_config, validate_config


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="A simple usage of the Telegram Bot API.",
                                         allow_abbrev=True)
    arg_parser.add_argument("--chat_id", type=str, help="sets the chat_id in settings")
    arg_parser.add_argument("--token", type=str, help="sets the bot token in settings")
    arg_parser.add_argument("--text", type=str, help="specifies the message to send to chat")
    args = arg_parser.parse_args()

    update_config(chat_id=args.chat_id, token=args.token)
    config = get_config()

    if not validate_config(config):
        raise Exception("Settings not valid. Use --token and --chat_id options to set settings entries.")

    if args.text:
        print(send_message(args.text))
