import logging
from .supabase import supabase
from telegram import Update

def add(queue_name: str, data: list, update: Update):
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
            metadata = {
                'user': {
                    'id': update.message.from_user.id,
                    'username': update.message.from_user.username,
                    'first_name': update.message.from_user.first_name,
                    'is_bot': update.message.from_user.is_bot,
                    'language_code': update.message.from_user.language_code
                },
                'chat': {
                    'id': update.message.chat.id,
                    'type': update.message.chat.type,
                    'username': update.message.chat.username,
                    'first_name': update.message.chat.first_name
                    },
                'message': {
                    'id': update.message.message_id,
                    'text': update.message.text,
                    'date': update.message.date.isoformat(),
                    'entities': [
                        {
                            'type': entity.type,
                            'offset': entity.offset,
                            'length': entity.length
                        } for entity in update.message.entities
                    ] if update.message.entities else []
                    }   
            }
            data = supabase.schema('pgmq_public').rpc('send', {
                'queue_name': queue_name,
                'message': {
                    'data': data,
                    'user': metadata['user'],
                    'chat': metadata['chat'],
                    'message': metadata['message']
                }
            }).execute()
            logging.info(f"Message sent to queue {queue_name}")
            logging.info(f"Message: {data}")
        return data.data
    except Exception as e:
        logging.error(f"Error sending message to queue {queue_name}: {e}")
        raise e

def add_links(links: list, update: Update):
    return add("link", links, update)
