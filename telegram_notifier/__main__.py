#!/usr/bin/python

import argparse
from . import *

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="A simple usage of the Telegram Bot API.", allow_abbrev=True
    )
    arg_parser.add_argument("--chat_id", type=str, help="sets the chat_id in settings")
    arg_parser.add_argument("--token", type=str, help="sets the bot token in settings")
    arg_parser.add_argument(
        "--message", type=str, help="specifies the message to send to chat"
    )
    arg_parser.add_argument(
        "--no_escape",
        action="store_true",
        required=False,
        help="do not escape special characters (e.g. '.', '-')",
    )
    args = arg_parser.parse_args()

    set_config_options(chat_id=args.chat_id, token=args.token)

    if args.message:
        if not validate_config(get_config()):
            raise InvalidConfigError(
                "Settings not valid. Use --token and --chat_id options to set settings entries."
            )
        if args.no_escape:
            print(send_message(args.message, args.no_escape))
        else:
            print(send_message(args.message))
    elif args.message == "":
        raise EmptyMessageError("Cannot use an empty string with --message option.")
