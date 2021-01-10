import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_telegram_notifier",
    version="0.0.2-3",
    author="Jonathan Townsend",
    description="Simple notifier utilizing the Telegram Bot API. This can be used by the " +
                "command line, by function call, or with a context manager.",
    install_requires=[
        "requests",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jon-edward/py-telegram-notifier",
    packages=setuptools.find_packages(include=[
        'telegram_notifier',
    ]),
    python_requires='>=3.6'
)
