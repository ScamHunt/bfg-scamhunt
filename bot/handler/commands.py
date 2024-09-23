from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import ScamHuntMessages as messages

from bot.onboarding.onboarding import onboarding_messages, OnboardingStates

from bot.db.user import get_user, create_user, User

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle scam reporting process."""
    markup= InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Show me an example", callback_data=OnboardingStates["EXAMPLE_START"]
                        )
                    ],
                    [
                        InlineKeyboardButton("Hunt on Facebook", url="https://www.facebook.com")
                    ],
                    [
                        InlineKeyboardButton(
                            "Hunt on Instagram", url="https://www.instagram.com"
                        )
                    ],
                ]
    )
    if update.message:
        await update.message.reply_text(
            messages.new_scam_report,
            parse_mode="Markdown",
            reply_markup=markup
        )
    else:
        await update.callback_query.message.edit_text(
            messages.new_scam_report,
            parse_mode="Markdown",
            reply_markup=markup
        )
    


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /learn command."""
    await update.message.reply_text(messages.learn, parse_mode="Markdown")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /help command."""
    await update.message.reply_text(messages.help)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = next(iter(OnboardingStates))
    user, _ = get_user(update.effective_user.id)
    if user is None:
        user = User(
            id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
        )
        create_user(user)
    message = onboarding_messages.get_message(state=state)
    await update.message.reply_text(message.text, reply_markup=message.keyboard)
