from telegram import Update


from telegram import Update
from urllib.parse import urlparse
import logging
from enum import Enum

from bot.link import instagram
from bot.link import facebook


def extract_phone_numbers(update: Update) -> tuple[list[str], list[str]]:
    entities = update.message.entities
    return [
        update.message.text[entity.offset : entity.offset + entity.length]
        for entity in entities
        if entity.type == "phone_number"
    ]


def extract_urls(update: Update) -> tuple[list[str], list[str]]:
    entities = update.message.entities
    urls = [
        update.message.text[entity.offset : entity.offset + entity.length]
        for entity in entities
        if entity.type == "url"
    ]
    return urls


class SocialMedia(Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    UNKNOWN = "unknown"


class Exceptions:
    UnknownPlatform = "We don't support this platform yet"


def extract_platform(link) -> SocialMedia:
    url = urlparse(link)
    domain = str.lower(url.netloc)
    if "instagram" in domain:
        return SocialMedia.INSTAGRAM
    elif "facebook" in domain:
        return SocialMedia.FACEBOOK
    else:
        return SocialMedia.UNKNOWN
