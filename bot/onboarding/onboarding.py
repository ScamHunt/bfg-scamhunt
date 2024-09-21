from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, ConversationHandler

from .onboarding_messages import OnboardingStates, OnboardingMessages, get_state
import logging

onboarding_messages = OnboardingMessages()


async def onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    state = get_state(query.data)
    message = onboarding_messages.get_message(state=state)
    if not message.keyboard:
        return await query.edit_message_text(message.text)
    await query.edit_message_text(message.text, reply_markup=message.keyboard)


def is_onboarding(state: str):
    return state in OnboardingStates.values()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = "WELCOME"
    message = onboarding_messages.get_message(state=state)
    await update.message.reply_text(message.text, reply_markup=message.keyboard)
