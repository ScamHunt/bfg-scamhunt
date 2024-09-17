
from telegram import Update

def extract_entities(update: Update) -> tuple[list[str], list[str]]:
    entities = update.message.entities
    phone_numbers = [update.message.text[entity.offset:entity.offset + entity.length] for entity in entities if entity.type == "phone_number"]
    urls = [update.message.text[entity.offset:entity.offset + entity.length] for entity in entities if entity.type == "url"]
    return phone_numbers, urls
