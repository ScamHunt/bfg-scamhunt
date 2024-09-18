from telegram import Update


def extract_phone_numbers(update: Update) -> tuple[list[str], list[str]]:
    entities = update.message.entities
    return [
        update.message.text[entity.offset : entity.offset + entity.length]
        for entity in entities
        if entity.type == "phone_number"
    ]


def extract_urls(update: Update) -> tuple[list[str], list[str]]:
    entities = update.message.entities
    urls = [
        update.message.text[entity.offset : entity.offset + entity.length]
        for entity in entities
        if entity.type == "url"
    ]
    return urls
