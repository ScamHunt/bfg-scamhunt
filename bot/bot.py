from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)

from dotenv import load_dotenv
import os
import bot.handler as handler

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(bot_token).build()

    application.add_handler(CallbackQueryHandler(handler.button_callback_handler))
    # Add the conversation handler to the application
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Entity("url"),
            handler.receive_link,
        )
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Entity("phone_number"),
            handler.receive_phone_number,
        )
    )
    application.add_handler(MessageHandler(filters.PHOTO, handler.receive_screenshot))

    # Add other handlers for independent commands
    application.add_handler(CommandHandler("report", handler.report))
    application.add_handler(CommandHandler("hunt", handler.report))
    application.add_handler(CommandHandler("start", handler.start))
    application.add_handler(CommandHandler("scamabout", handler.scamabout))
    application.add_handler(CommandHandler("mystats", handler.mystats))
    application.add_handler(CommandHandler("leaderboard", handler.leaderboard))
    application.add_handler(CommandHandler("help", handler.help_command))
    application.add_handler(CommandHandler("learn", handler.learn))

    # Error handler
    application.add_error_handler(handler.error_handler)

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()
