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


class ScamType(Enum):
    PHONE_NUMBER = auto()
    SCREENSHOT = auto()
    LINK = auto()
    TEXT = auto()


class CallbackData:
    CANCEL = "cancel"
    CONFIRM = "confirm"
    YES = "yes"
    NO = "no"
    REPORT_SCAM = "report_scam"


class BotStates(Enum):
    START = auto()
    RECEIVE_SCREENSHOT = auto()
    RECEIVE_PHONE_NUMBER = auto()
    RECEIVE_LINK = auto()
    RECEIVE_TEXT = auto()


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle errors."""
    logging.error(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text(messages.error)
    elif update.callback_query:
        await update.callback_query.message.edit_text(messages.error)


def get_inline_cancel_confirm_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Confirm ✅", callback_data=CallbackData.CONFIRM),
                InlineKeyboardButton("Cancel ❌", callback_data=CallbackData.CANCEL),
            ],
        ]
    )
