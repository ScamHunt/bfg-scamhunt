from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from dotenv import load_dotenv
import os
import logging

import bot.handler.callbacks as callbacks
import bot.handler.commands as commands
import bot.handler.receiver as receiver
import bot.handler.utils as utils


load_dotenv(override=True)

if os.getenv("ENV") == "local":
    bot_token = os.getenv("TELEGRAM_STG_BOT_TOKEN")
else:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(bot_token).build()

    application.add_handler(CallbackQueryHandler(callbacks.button))
    # Add the conversation handler to the application
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Entity("url"),
            receiver.link,
        )
    )
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Entity("phone_number"),
            receiver.phone_number,
        )
    )
    application.add_handler(MessageHandler(filters.PHOTO, receiver.screenshot))

    # Add other handlers for independent commands
    application.add_handler(CommandHandler("report", commands.report))
    application.add_handler(CommandHandler("hunt", commands.report))
    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("help", commands.help))
    application.add_handler(CommandHandler("learn", commands.learn))

    # Error handler
    application.add_error_handler(utils.error)

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()
