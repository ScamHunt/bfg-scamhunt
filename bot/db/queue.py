import logging
from .supabase import supabase


def add(queue_name: str, data: list):
    """Add a message to a queue using Supabase RPC call.
    
    Args:
        queue_name (str): Name of the queue to send to. Defaults to "link".
        links (list): List of links to add to the queue. Defaults to empty list.
        
    Returns:
        The response data from the RPC call
        
    Raises:
        Exception: If there is an error sending the message to the queue
    """
    try:
        if data:
            data = supabase.schema('pgmq_public').rpc('send', {
                'queue_name': queue_name,
                'message': {
                    'data': data
                }
            }).execute()
        return data.data
    except Exception as e:
        logging.error(f"Error sending message to queue {queue_name}: {e}")
        raise e

def add_links(links: list):
    return add("link", links)

