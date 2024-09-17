from aiograpi import Client
from aiograpi.types import Media


cl = Client()


async def extract_post_info(code) -> Media:
        media_pk = await cl.media_pk_from_code(code)
        media_info = await cl.media_info(media_pk)
        return media_info


