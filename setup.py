import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_telegram_notifier",
    version="0.2.3",
    author="Jonathan Townsend",
    description="A simple notifier for sending a message to a Telegram chat using the Telegram Bot API.",
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
    python_requires=">=3.8",
)
