from .supabase import supabase
import logging

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



def search_embeddings(embedding: list[float]) :
    try:
        data = supabase.rpc("search_embeddings", {"query_embed": embedding ,"threshold": 0.7}).execute()
        print(data)
        return data
    except Exception as e:
        logger.error("Error searching embeddings: %s", e)
        return []