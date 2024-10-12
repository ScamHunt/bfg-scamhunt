from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import ScamHuntMessages as messages

from bot.onboarding.onboarding import onboarding_messages, OnboardingStates

from bot.db.user import create_user_if_not_exists, get_user
from bot.db.report import get_leaderboard

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.user_metrics import track_user_event, Event
from bot.feedback import feedback_messages, FeedbackStates
from bot.db.user import is_banned


@is_banned
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle scam reporting process."""
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Show me an example",
                    callback_data=OnboardingStates["EXAMPLE_START"],
                )
            ],
            [InlineKeyboardButton("Hunt on Facebook", url="https://www.facebook.com")],
            [
                InlineKeyboardButton(
                    "Hunt on Instagram", url="https://www.instagram.com"
                )
            ],
        ]
    )
    if update.message:
        await update.message.reply_text(
            messages.new_scam_report, parse_mode="Markdown", reply_markup=markup
        )
    else:
        await update.callback_query.message.edit_text(
            messages.new_scam_report, parse_mode="Markdown", reply_markup=markup
        )


@is_banned
async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /learn command."""
    track_user_event(update, context, Event.LEARN)
    await update.message.reply_text(messages.learn, parse_mode="Markdown")


@is_banned
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /help command."""
    track_user_event(update, context, Event.HELP)
    await update.message.reply_text(messages.help)


@is_banned
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user_event(update, context, Event.START)
    state = next(iter(OnboardingStates))
    create_user_if_not_exists(update, context)
    message = onboarding_messages.get_message(state=state)
    await update.message.reply_text(message.text, reply_markup=message.keyboard)


@is_banned
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /feedback command."""
    context.user_data["state"] = FeedbackStates.FEEDBACK_SCORE
    message = feedback_messages.get_message(state=context.user_data["state"])
    if update.message:
        await update.message.reply_text(message.text, reply_markup=message.keyboard)
    else:
        await update.callback_query.message.edit_text(
            message.text, reply_markup=message.keyboard
        )

@is_banned
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaderboard = get_leaderboard()[:10]
    leaderboard_text = "Leaderboard:\n" if leaderboard else "No reports have been made yet.\n"
    for entry in leaderboard:
        user, _ = get_user(entry["user_id"])
        user.username = user.username or user.first_name or user.last_name or '******'
        leaderboard_text += f"👑 {user.username[:-2] + '**'}: {entry['report_count']} reports\n"
    await update.message.reply_text(leaderboard_text)