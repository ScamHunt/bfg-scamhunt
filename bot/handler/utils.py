from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
import logging


from enum import Enum, auto
from bot.messages import ScamHuntMessages as messages

# Initialize the ScamHuntMessages class

class CallbackData:
    CANCEL = "cancel"
    CONFIRM = "confirm"
    YES = "yes"
    NO = "no"
    REPORT_SCAM = "report_scam"
    FEEDBACK = "feedback"
    UNSURE = "unsure"


class BotStates(Enum):
    START = auto()
    RECEIVE_SCREENSHOT = auto()
    RECEIVE_PHONE_NUMBER = auto()
    RECEIVE_LINK = auto()
    RECEIVE_TEXT = auto()


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logging.error(f"Error occurred: {context.error}", exc_info=context.error)
    logging.error(f"Update that caused the error: {update}")

    # Handle the case where update is NoneType
    if not update:
        await context.bot.send_message(chat_id=context._chat_id, text=messages.error)
        return

    if update.effective_user:
        user_info = f"User ID: {update.effective_user.id}, Username: {update.effective_user.username}"
        logging.error(f"User information: {user_info}")

    if update.effective_chat:
        chat_info = f"Chat ID: {update.effective_chat.id}, Chat Type: {update.effective_chat.type}"
        logging.error(f"Chat information: {chat_info}")

    if update.message:
        logging.error(f"Message text: {update.message.text}")
        await update.message.reply_text(messages.error)

    elif update.callback_query:
        logging.error(f"Callback query data: {update.callback_query.data}")
        await update.callback_query.message.edit_text(messages.error)


def get_inline_cancel_confirm_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Report as scam ✅", callback_data=CallbackData.CONFIRM
                ),
                InlineKeyboardButton(
                    "Don't report ❌", callback_data=CallbackData.CANCEL
                ),
            ],
        ]
    )


def get_inline_keyboard_for_scam_result():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👍 Yes", callback_data=CallbackData.YES),
                InlineKeyboardButton("👎 No", callback_data=CallbackData.NO),
                InlineKeyboardButton("🤔 Unsure", callback_data=CallbackData.UNSURE),
            ],
        ]
    )
