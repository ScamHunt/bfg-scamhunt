from aiograpi import Client
from aiograpi.types import Media, UserShort
from aiograpi.exceptions import PleaseWaitFewMinutes
from telegram import Update
from telegram.constants import ParseMode
from urllib.parse import urlparse
import logging
import re


cl = Client()


def extract_post_id(link) -> str:
    url = urlparse(link)
    match = re.search(r'/p/([^/?#&]+)', url.path)
    if match:
        return match.group(1)
    return None


async def extract_post_info(code) -> Media:
        media_pk = await cl.media_pk_from_code(code)
        media_info = await cl.media_info(media_pk)
        return media_info


async def handle_instagram(update: Update, link: str):
    await update.message.reply_text(
        f"I've detected an Instagram link in your message: {link}\n"
        "Let me analyse it further..."
    )
    try:
        post_id = extract_post_id(link)
        info = await extract_post_info(post_id)
        await update.message.reply_text("I've extracted the following information from this post:\n"
                                        f"*Username*: {info.user.username}\n"
                                        f"*Caption*: ```\n{info.caption_text}\n```\n",
                                        parse_mode=ParseMode.MARKDOWN)
    except PleaseWaitFewMinutes as e:
        logging.error(e)
        if e.require_login:
            await update.message.reply_text(
                "This Instagram post is private, you can try submitting a screenshot instead.")
        else:
            await update.message.reply_text(
                "I could not analyse this link right now, you can try again later.")
