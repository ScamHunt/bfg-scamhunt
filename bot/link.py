from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import re
from urllib.parse import urlparse
import logging
from dataclasses import dataclass
from enum import Enum

from . import instagram
from . import facebook


class SocialMedia(Enum):
    FACEBOOK = 1
    INSTAGRAM = 2
    UNKNOWN = 3


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


# Function to handle the incoming link
async def extract_data(link):
    logging.info(f"Received link: {link}")

    platform = extract_platform(link)

    if platform == SocialMedia.INSTAGRAM:
        return await instagram.handle(link)
    elif platform == SocialMedia.FACEBOOK:
        return await facebook.handle(link)
    else:
        return (None, Exceptions.UnknownPlatform)
