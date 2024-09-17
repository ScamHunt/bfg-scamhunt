from aiograpi import Client
from aiograpi.types import Media, UserShort
from aiograpi.exceptions import PleaseWaitFewMinutes, LoginRequired
from telegram import Update
from telegram.constants import ParseMode
from urllib.parse import urlparse
import logging
import re


cl = Client()


async def handle_instagram(update: Update, link: str):
    await update.message.reply_text(
        f"I've detected an Instagram link in your message: {link}\n"
        "Let me analyse it further..."
    )
    try:
        media_pk = await cl.media_pk_from_url(link)
        logging.debug(f"Extracted media_pk: {media_pk}")
        if not media_pk:
            await update.message.reply_text("I could not extract the post ID from this link, please try again with a valid Instagram post link.")
            return
        post = await cl.media_info(media_pk)
        await update.message.reply_text("I've extracted the following information from this post:\n"
                                        f"<b>Username</b>: {post.user.username}\n"
                                        f"<b>Type</b>: {post.media_type}\n"
                                        f"<b>Caption</b>: <pre>{post.caption_text}</pre>\n",
                                        parse_mode=ParseMode.HTML) # Careful with Markdown, causes errors because of unescaped chars
    except LoginRequired as e:
        logging.error(e)
        await update.message.reply_text("This Instagram post is private, try submitting a screenshot instead.")
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("I could not analyse this link right now, you can try again later.")
