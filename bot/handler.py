from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from .utils import extract_entities
import logging
from .link import handle_link
from .instagram import extract_post_info
import json

REPORT_TYPE, DETAILS, CONFIRMATION = range(3)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# Command Handlers
# Function for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_animation(
        animation=open('assets/gifs/pudgy_scam.gif', 'rb'),
        caption=f"Hello {update.effective_user.first_name}!\n"
                "Welcome to the ScamHunt Bot!\n"
                "I'm here to help you report scams and protect yourself and others from them.\n"
                "Please use the /report command to start reporting a scam.")
    

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ['/report', '/info'],
        ['/stats', '/help']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Main Menu:\n"
        "/report - Report a new scam\n"
        "/info - Get information about common scams\n"
        "/stats - View scam statistics\n"
        "/help - Get help using this bot",
        reply_markup=reply_markup
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: Add more information about scams
    await update.message.reply_text(
        "Common types of scams:\n"
        "1. Phishing emails\n"
        "2. Phone scams\n"
        "3. Online shopping fraud\n"
        "4. Investment scams\n"
        "5. Romance scams\n\n"
        "Always be cautious and verify before sharing personal information or money."
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: Fetch stats from the database
    await update.message.reply_text(
        "Scam Report Statistics:\n"
        "Total reports: 1,234\n"
        "Most common type: Phishing emails\n"
        "Reports this week: 56\n\n"
        "Thank you for helping to combat scams!"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: Add more information about how to use the bot
    await update.message.reply_text(
        "How to use this bot:\n"
        "1. Use /report to start reporting a scam\n"
        "2. Follow the prompts to provide details\n"
        "3. Use /info to learn about common scams\n"
        "4. Use /stats to view scam statistics\n"
        "5. Use /menu to see all available commands\n\n"
        "If you need further assistance, please contact @ibrahim_scamhunt"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Scam report cancelled. If you want to report a scam in the future, just send /report.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Conversation Handlers
async def handle_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Message Scam', 'Phone Call Scam'], 
                ['Email Scam', 'Website Scam'],
                ['Facebook Scam', 'Instagram Scam'],
                ['Carousell Scam', 'TikTok Scam'],
                ['Other Scam']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Welcome to the Scam Reporter Bot! What type of scam would you like to report?",
        reply_markup=reply_markup
    )
    return REPORT_TYPE

async def handle_report_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['scam_type'] = update.message.text
    await update.message.reply_text(
        f"You're reporting a {update.message.text}. Please provide more details about the scam.\nSend /cancel if you want to cancel the report.\n Send /confirm if you want to confirm the report.",
        reply_markup=ReplyKeyboardRemove()
    )
    return DETAILS

async def handle_report_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_numbers, links = extract_entities(update)
    context.user_data['phone_numbers'] = phone_numbers
    context.user_data['links'] = links
    message = f"You've provided the following details:\n"
    if phone_numbers:
        message += f"Phone Numbers: {', '.join(phone_numbers)}\n"
    if links:
        message += f"Links: {', '.join(links)}\n"
    message += "Send /confirm if you want to confirm the report.\n"
    message += "Send /cancel if you want to cancel the report."
    await update.message.reply_text(
        message
    )
    return CONFIRMATION

async def handle_report_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scam_type = context.user_data.get('scam_type', 'Unknown')
    details = update.message.text
    # Here you would typically save the report to a database
    await update.message.reply_text(
        f"Thank you for reporting this {scam_type}. Your report has been recorded.\n\n"
        "Remember:\n"
        "• Never share personal information with strangers\n"
        "• Be cautious of unsolicited offers or requests\n"
        "• If it sounds too good to be true, it probably is\n\n"
        "Stay safe and thank you for helping to combat scams!"
    )
    return ConversationHandler.END

async def handle_attachment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attachment_type = "Attachment"
    if update.message.document:
        attachment_type = "Document"
    elif update.message.photo:
        attachment_type = "Photo"
    elif update.message.audio:
        attachment_type = "Audio"
    elif update.message.video:
        attachment_type = "Video"
    elif update.message.voice:
        attachment_type = "Voice"
    elif update.message.video_note:
        attachment_type = "Video Note"
    
    await update.message.reply_text(
        f"You've shared a {attachment_type}. This could be valuable evidence.\n"
        "Please also provide a text description of the scam you're reporting."
    )

async def handle_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_numbers, links = extract_entities(update)
    if not phone_numbers and not links:
        await update.message.reply_text(
            "I couldn't detect any phone numbers or links in your message. "
            "If you're trying to report a scam, please use the /report command."
        )
    for number in phone_numbers:
        await update.message.reply_text(
            f"I've detected a phone number in your message: {number}\n"
        )
    for link in links:
        await handle_link(update, link)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"An error occurred: {context.error}")
    await update.message.reply_text(
        f"An error occurred\n"
        "I apologize for the inconvenience. Please try again later or contact support."
    )
