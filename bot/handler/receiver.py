from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import ScamHuntMessages as messages
from bot.handler.utils import BotStates, ScamType
from bot.extractors import extract_urls
from bot.extractors import extract_phone_numbers
from bot.handler.utils import get_inline_cancel_confirm_keyboard
from bot.extractors import extract_platform, SocialMedia
from bot.messages import ScamHuntMessages as messages


async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a phone number for a scam."""
    phone_numbers = extract_phone_numbers(update)
    context.user_data["scam_type"] = ScamType.PHONE_NUMBER
    phone_numbers = ", ".join(phone_numbers)
    await update.message.reply_text(
        messages.phone_number_sharing.replace("<phone_number>", phone_numbers),
        reply_markup=get_inline_cancel_confirm_keyboard(),
        parse_mode="Markdown",
    )


async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a screenshot for a scam."""
    context.user_data["state"] = BotStates.RECEIVE_SCREENSHOT
    context.user_data["photo"] = update.message.photo[-1]
    message = await update.message.reply_text(
        messages.screenshot_sharing,
        parse_mode="Markdown",
        reply_markup=get_inline_cancel_confirm_keyboard(),
    )


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a link for a scam."""
    context.user_data["state"] = BotStates.RECEIVE_LINK
    context.user_data["link"] = update.message.text
    await update.message.reply_text(
        messages.link_sharing,
        reply_markup=get_inline_cancel_confirm_keyboard(),
        parse_mode="Markdown",
    )


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle text messages."""
    await update.message.reply_text(messages.text_sharing)
