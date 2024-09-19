from aiograpi import Client
from aiograpi.types import Media, UserShort
from aiograpi.exceptions import PleaseWaitFewMinutes, LoginRequired
from urllib.parse import urlparse
import logging
import re
from instaloader import Instaloader, Post, BadResponseException


cl = Client()
L = Instaloader()


class Exceptions:
    InvalidInstagramLink = "Invalid Instagram link"
    PrivateInstagramPost = "Private Instagram post"
    InstagramAnalysisError = "Error analyzing Instagram post"


class Data:
    def __init__(self, username: str, caption: str):
        self.username = username
        self.caption = caption

    def __str__(self):
        return f"Username: {self.username}\nCaption: {self.caption}"


async def handle(link: str) -> tuple[Data, Exceptions]:
    """Try to extract data using Instaloader first, then fallback to aiograpi."""
    logging.info("Trying to extract data using instaloader")
    data, _ = try_instaloader(link)
    if data is not None:
        return (data, None)
    logging.info("Trying to extract data using aiograpi")
    return await try_aiograpi(link)


async def try_aiograpi(link: str) -> tuple[Data, Exceptions]:
    """Extract data using aiograpi."""
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


def try_instaloader(link: str) -> tuple[Data, Exceptions]:
    """Extract data using Instaloader."""
    try:
        post_id = extract_post_id(link)
        logging.debug(f"Extracted post_id: {post_id}")
        if post_id is None:
            return (None, Exceptions.InvalidInstagramLink)
        post = Post.from_shortcode(L.context, post_id)
        logging.debug(f"Extracted post: {post}")
        return (
            Data(
                username=post.owner_username,
                caption=post.caption,
            ),
            None,
        )
    except BadResponseException as e:
        logging.error(e)
        return (None, Exceptions.PrivateInstagramPost)
    except Exception as e:
        logging.error(e)
        return (None, Exceptions.InstagramAnalysisError)


def extract_post_id(link: str) -> str:
    """Extract the post id from the instagram url."""
    url = urlparse(link)
    path = url.path
    post_id = re.search(r"p/([^/]+)", path)
    return post_id.group(1)
