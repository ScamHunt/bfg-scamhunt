

from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import ScamHuntMessages as messages

from bot.onboarding.onboarding import onboarding_messages

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle scam reporting process."""
    await update.message.reply_text(messages.new_scam_report)


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /learn command."""
    await update.message.reply_text(messages.learn, parse_mode="Markdown")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /help command."""
    await update.message.reply_text(messages.help)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = "WELCOME"
    message = onboarding_messages.get_message(state=state)
    await update.message.reply_text(message.text, reply_markup=message.keyboard)
