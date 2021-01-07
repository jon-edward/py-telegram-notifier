import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-telegram-notifier",
    version="0.0.1",
    author="Jonathan Townsend",
    description="Sends a message to a Telegram Bot using the Telegram bot API. This can be done by the "
                "command line, by a send_message method call, or with a context manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jon-edward/py-telegram-notifier",
    packages=setuptools.find_packages(include=['notifier']),
    python_requires='>=3.6'
)
