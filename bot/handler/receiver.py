from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import ScamHuntMessages as messages
from bot.handler.utils import BotStates, ScamType
from bot.utils import extract_urls
from bot.utils import extract_phone_numbers
from bot.handler.utils import get_inline_cancel_confirm_keyboard
import bot.link as link
from bot.messages import ScamHuntMessages as messages


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a link for a scam."""
    links = extract_urls(update)
    links = ", ".join(links)
    await update.message.reply_text(messages.link_sharing.replace("<link>", links))
    # Simulate analysis
    context.user_data["link"] = links
    data, exception = await link.extract_data(links)
    if data:
        await update.message.reply_text(
            str(data), reply_markup=get_inline_cancel_confirm_keyboard()
        )
    else:
        await update.message.reply_text(exception + messages.end_message)


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


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle text messages."""
    await update.message.reply_text(messages.text_sharing)
