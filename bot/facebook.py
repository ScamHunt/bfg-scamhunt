from telegram import Update


class Exceptions:
    NotImplementedError = "Facebook is not implemented yet"


class Data:
    def __init__(self, username: str, caption: str):
        self.username = username
        self.caption = caption


def handle(link: str) -> Data | Exceptions:
    return None, Exceptions.NotImplementedError
