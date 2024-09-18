from aiograpi import Client
from aiograpi.types import Media, UserShort
from aiograpi.exceptions import PleaseWaitFewMinutes, LoginRequired
from urllib.parse import urlparse
import logging
import re


cl = Client()


class Exceptions:
    InvalidInstagramLink = "Invalid Instagram link"
    PrivateInstagramPost = "Private Instagram post"
    InstagramAnalysisError = "Error analyzing Instagram post"


class Data:
    def __init__(self, username: str, caption: str):
        self.username = username
        self.caption = caption


async def handle(link: str) -> tuple[Data, Exceptions]:
    try:
        media_pk = await cl.media_pk_from_url(link)
        logging.debug(f"Extracted media_pk: {media_pk}")
        if not media_pk:
            return (None, Exceptions.InvalidInstagramLink)
        post = await cl.media_info(media_pk)
        return (Data(post.user.username, post.caption_text), None)

    except LoginRequired as e:
        logging.error(e)
        return (None, Exceptions.PrivateInstagramPost)
    except Exception as e:
        logging.error(e)
        return (None, Exceptions.InstagramAnalysisError)
