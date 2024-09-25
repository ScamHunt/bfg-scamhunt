from pydantic import BaseModel
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
from typing import Union


load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)


class Embedding(BaseModel):
    text: str
    embedding: list[float]


async def get_embedding(text: str) -> Union[Embedding, Exception]:
    logger.info(f"Getting embedding for text {text}")
    try:
        response = client.embeddings.create(
            model="text-embedding-3-large", input=text, dimensions=256
        )
    except Exception as e:
        logger.error(f"Error getting embedding: {e}")
        return (None, e)
    else:
        logger.info(f"Got embedding for text")
    return (Embedding(text=text, embedding=response.data[0].embedding), None)
