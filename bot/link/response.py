from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import re


# TODO: extract link info
def extract_link_data(link):
    pass


# Function to handle the incoming link
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    
    # Regex to detect a URL in the message
    url_pattern = r"(https?://[^\s]+)"
    urls = re.findall(url_pattern, message_text)
    
    if urls:
        # If a link is found, ask a follow-up question
        await update.message.reply_text("Thanks for sharing the link! Can you provide more details about why you think this might be a scam?")
    else:
        # If no link is found, inform the user
        await update.message.reply_text("Please share a valid link so I can help you!")
