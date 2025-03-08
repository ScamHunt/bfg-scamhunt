from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import ScamHuntMessages as messages
from bot.handler.utils import BotStates
from bot.extractors import extract_urls
from bot.extractors import extract_phone_numbers
from bot.handler.utils import get_inline_cancel_confirm_keyboard
from bot.extractors import extract_platform, SocialMedia
from bot.messages import ScamHuntMessages as messages
from bot.db.user import is_banned
from bot.db import queue
import logging

@is_banned
async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a phone number for a scam."""
    phone_numbers = extract_phone_numbers(update)
    phone_numbers = ", ".join(phone_numbers)
    await update.message.reply_text(
        messages.phone_number_sharing.replace("<phone_number>", phone_numbers),
        parse_mode="Markdown",
    )


@is_banned
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a screenshot for a scam."""
    context.user_data["state"] = BotStates.RECEIVE_SCREENSHOT
    context.user_data["photo"] = update.message.photo[-1]
    message = await update.message.reply_text(
        messages.screenshot_sharing,
        parse_mode="Markdown",
        reply_markup=get_inline_cancel_confirm_keyboard(),
    )

@is_banned
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a link for a scam."""
    context.user_data["state"] = BotStates.RECEIVE_LINK
    context.user_data["links"] = extract_urls(update)
    logging.info(f"Received links: {context.user_data['links']}")
    result = queue.add_links(context.user_data["links"])
    logging.info(f"Added to queue: {result}")
    
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            messages.confirm,
            parse_mode="Markdown",
        )

@is_banned
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle text messages."""
    await update.message.reply_text(messages.text_sharing)
