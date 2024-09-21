from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, ConversationHandler
from .utils import extract_urls, extract_phone_numbers
import logging

from . import link
from .messages import ScamHuntMessages
import json
import mimetypes
from .openai.ocr import ocr_image, Screenshot

from .db.supabase import supabase, upload_to_supabase

from enum import Enum, auto
from .db.report import Report, create_report
from .onboarding.onboarding import is_onboarding, onboarding, start
from .onboarding.onboarding_messages import OnboardingStates

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Initialize the ScamHuntMessages class
messages = ScamHuntMessages()


class CallbackData:
    REPORT_SCAM = "report_scam"
    WEBSITE_SCAM = "website_scam"
    FACEBOOK_SCAM = "facebook_scam"
    INSTAGRAM_SCAM = "instagram_scam"
    CAROUSELL_SCAM = "carousell_scam"
    TIKTOK_SCAM = "tiktok_scam"
    MESSAGE_SCAM = "message_scam"
    EMAIL_SCAM = "email_scam"
    OTHER_SCAM = "other_scam"
    CANCEL = "cancel"
    CONFIRM = "confirm"
    YES = "yes"
    NO = "no"


class BotStates(Enum):
    START = auto()
    REPORT = auto()
    RECEIVE_LINK = auto()
    RECEIVE_PHONE_NUMBER = auto()
    RECEIVE_SCREENSHOT = auto()
    RECEIVE_TEXT = auto()
    SCAMABOUT = auto()
    MYSTATS = auto()
    LEADERBOARD = auto()


class ScamType(Enum):
    PHONE_NUMBER = auto()
    SCREENSHOT = auto()
    LINK = auto()
    TEXT = auto()


async def button_callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle the callback query from the inline keyboard."""
    if is_onboarding(update.callback_query.data):
        await onboarding(update, context)
        return
    query = update.callback_query
    await query.answer()
    scam_type = context.user_data.get("scam_type")
    match query.data:
        case CallbackData.REPORT_SCAM:
            await query.edit_message_text(
                text=messages.new_scam_report, parse_mode="Markdown"
            )
        case CallbackData.FACEBOOK_SCAM:
            await query.edit_message_text(
                text=messages.facebook_scam,
                parse_mode="Markdown",
                reply_markup=get_inline_cancel_confirm_keyboard(),
            )

        case CallbackData.INSTAGRAM_SCAM:
            await query.edit_message_text(
                text=messages.instagram_scam,
                parse_mode="Markdown",
                reply_markup=get_inline_cancel_confirm_keyboard(),
            )
        case CallbackData.OTHER_SCAM:
            await query.edit_message_text(
                text=messages.other_scam,
                parse_mode="Markdown",
                reply_markup=get_inline_cancel_confirm_keyboard(),
            )
        case CallbackData.CANCEL:
            await query.edit_message_text(
                text=messages.cancel + messages.end_message,
                parse_mode="Markdown",
            )
        case CallbackData.CONFIRM:
            logging.info(context.user_data)
            match context.user_data["state"]:
                case BotStates.RECEIVE_SCREENSHOT:
                    await query.edit_message_text(
                        text=messages.looking_into_scam,
                        parse_mode="Markdown",
                    )
                    image = await context.bot.get_file(
                        context.user_data["photo"].file_id
                    )
                    result, exception = await ocr_image(image)
                    if exception:
                        await query.edit_message_text(
                            text=exception + messages.end_message,
                            parse_mode="Markdown",
                        )
                    context.user_data["state"] = BotStates.START
                    await query.edit_message_text(
                        result.description,
                        reply_markup=get_inline_cancel_confirm_keyboard(),
                    )
                case _:
                    await query.edit_message_text(
                        text=messages.confirm + messages.end_message,
                        parse_mode="Markdown",
                    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle scam reporting process."""
    await update.message.reply_text(messages.new_scam_report)


async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


async def receive_phone_number(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Handle when user sends a phone number for a scam."""
    phone_numbers = extract_phone_numbers(update)
    context.user_data["scam_type"] = ScamType.PHONE_NUMBER
    phone_numbers = ", ".join(phone_numbers)
    await update.message.reply_text(
        messages.phone_number_sharing.replace("<phone_number>", phone_numbers),
        reply_markup=get_inline_cancel_confirm_keyboard(),
        parse_mode="Markdown",
    )


async def receive_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle when user sends a screenshot for a scam."""
    context.user_data["state"] = BotStates.RECEIVE_SCREENSHOT
    context.user_data["photo"] = update.message.photo[-1]
    message = await update.message.reply_text(
        messages.screenshot_sharing,
        parse_mode="Markdown",
        reply_markup=get_inline_cancel_confirm_keyboard(),
    )


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle text messages."""
    await update.message.reply_text(messages.text_sharing)


async def scamabout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /scamabout command where users provide more scam details."""

    await update.message.reply_text(messages.scamabout)


async def mystats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /mystats command."""
    await update.message.reply_text(messages.leadership)


async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /leaderboard command."""
    await update.message.reply_text(messages.leadership)


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /learn command."""
    await update.message.reply_text(messages.learn, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /help command."""
    await update.message.reply_text(messages.help)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle errors."""
    logging.error(f"Update {update} caused error {context.error}")
    if update:
        await update.message.reply_text(messages.error)


def get_inline_cancel_confirm_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Confirm ✅", callback_data=CallbackData.CONFIRM),
                InlineKeyboardButton("Cancel ❌", callback_data=CallbackData.CANCEL),
            ],
        ]
    )


def get_inline_yes_no_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Yes ✅", callback_data=CallbackData.YES),
                InlineKeyboardButton("No ❌", callback_data=CallbackData.NO),
            ],
        ]
    )
