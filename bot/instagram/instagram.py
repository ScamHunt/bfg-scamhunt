from aiograpi import Client, Media
import asyncio


cl = Client()


async def get_post_info(code) -> asyncio.coroutine:
    media_pk = await cl.media_pk_from_code(code)
    media_info = await cl.media_info(media_pk)
    return media_info


# media = asyncio.run(get_post_info('C_3I-uETi9C'))
# print(media)
