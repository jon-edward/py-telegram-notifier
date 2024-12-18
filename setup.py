import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_telegram_notifier",
    version="1.0.0",
    author="Jonathan Townsend",
    description="A tool using the Telegram Bot API for sending messages to a Telegram chat by a context manager, function call, or CLI.",
    install_requires=[
        "requests",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jon-edward/py-telegram-notifier",
    packages=setuptools.find_packages(
        include=[
            "telegram_notifier",
        ]
    ),
    python_requires=">=3.7",
)
