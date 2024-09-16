
from telegram import Update

def extract_entities(update: Update) -> tuple[list[str], list[str]]:
    entities = update.message.entities
    phone_numbers = [update.message.text[entity.offset:entity.offset + entity.length] for entity in entities if entity.type == "phone_number"]
    urls = [update.message.text[entity.offset:entity.offset + entity.length] for entity in entities if entity.type == "url"]
    return phone_numbers, urls


def classify_link(link: str) -> str:
    if "facebook.com" in link:
        return "facebook"
    elif "instagram.com" in link:
        return "instagram"
    elif "twitter.com" in link:
        return "twitter"
    else:
        return "unknown"

def is_scam(link: str) -> bool:
    # TODO: check if link is malicious using VirusTotal
    return True