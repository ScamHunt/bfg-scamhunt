from .supabase import supabase
import logging
from pydantic import BaseModel

class Embedding(BaseModel):
    id: int
    similarity: float

logger = logging.getLogger(__name__)




def insert_embedding(embedding: list[float], report_id: int) -> None:
    print("report_id", report_id)
    try:
        supabase.table("report_embedding").insert(
            {"embeddings": embedding, "report_id": report_id}
        ).execute()
    except Exception as e:
        logger.error("Error inserting embedding: %s", e)
    pass



def search_embeddings(embedding: list[float]) -> list[Embedding] | list:
    try:
        data = supabase.rpc("embeddings_query", {"match_threshold":0.7,"query_embedding":embedding}).execute()
        return data.data
    except Exception as e:
        logger.error("Error searching embeddings: %s", e)
        return []