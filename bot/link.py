from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import re
from urllib.parse import urlparse
import logging
from dataclasses import dataclass
from enum import Enum


class SocialMedia(Enum):
    FACEBOOK = 1
    INSTAGRAM = 2
    UNKNOWN = 3


@dataclass
class LinkInfo:
    social_media: SocialMedia
    post_id: str | None


def extract_post_id(link) -> str:
    match = re.search(r'/p/([^/?#&]+)', link)
    if match:
        return match.group(1)
    return None


def extract_link_data(link) -> LinkInfo:
    url = urlparse(link)
    domain = str.lower(url.netloc)
    if (domain.find('instagram')):
        return LinkInfo(SocialMedia.INSTAGRAM, extract_post_id(url.path))
    elif (domain.find('facebook')):
        return LinkInfo(SocialMedia.FACEBOOK, None)
    else:
        return LinkInfo(SocialMedia.UNKNOWN, None)


# Function to handle the incoming link
async def handle_link(link):
    logging.info(f'Received link: {message_text}')

    try:
        link_info = extract_link_data(message_text)
        sm = link_info.social_media
        if sm == SocialMedia.INSTAGRAM:
            await update.message.reply_text(f"Thanks for sharing the Instagram link! The post ID is {link_info.post_id}, I will check it for you")
        else:
            await update.message.reply_text(f"Thanks for sharing the link, but it is not supported right now")
    except:
        await update.message.reply_text("Mmh... this link seems to be invalid")
