from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import re
from urllib.parse import urlparse
import logging
from dataclasses import dataclass
from enum import Enum
from .instagram import handle_instagram


class SocialMedia(Enum):
    FACEBOOK = 1
    INSTAGRAM = 2
    UNKNOWN = 3


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
async def handle_link(update: Update, link):
    logging.info(f"Received link: {link}")

    platform = extract_platform(link)

    if platform == SocialMedia.INSTAGRAM:
        await handle_instagram(update, link)
    elif platform == SocialMedia.FACEBOOK:
        await update.message.reply_text(
            "I am unable to analyse Facebook links for now, please be cautious."
        )
    else:
        await update.message.reply_text(
            "I am unable to analyse this platform for now, please be cautious."
        )
