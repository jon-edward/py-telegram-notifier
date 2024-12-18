#!/usr/bin/python

import argparse
import logging

from notifier import Notifier


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Send a message to a Telegram chat.", allow_abbrev=True
    )

    arg_parser.add_argument(
        "message", type=str, help="specifies the message to send to chat"
    )

    args = arg_parser.parse_args()

    if args.message:
        Notifier().send_message(args.message)
    else:
        logging.error("No message specified.")
        arg_parser.print_help()
