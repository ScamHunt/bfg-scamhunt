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

    # Define a ConversationHandler with states and callback functions
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handler.start), 
                      CommandHandler('hunt', handler.report), 
                      CommandHandler('report', handler.report), 
                      MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Entity("url"), handler.receive_link),
                      MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Entity("phone_number"), handler.receive_phone_number),
                      ],
        states={
            handler.REPORT: [
                CommandHandler('report', handler.report),
                CommandHandler('hunt', handler.report),
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Entity("url"), handler.receive_link),
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Entity("phone_number"), handler.receive_phone_number),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.link_unsure),
                MessageHandler(filters.PHOTO, handler.receive_screenshot)
            ],
            handler.SCAMABOUT: [
                CommandHandler('scamabout', handler.scamabout)
            ],
            handler.FEEDBACK: [
                CommandHandler('feedback', handler.feedback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.receive_feedback)
            ],
            handler.COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.comment)
            ],
            handler.LEARN: [
                CommandHandler('learn', handler.learn)
            ],
        },
        fallbacks=[CommandHandler('cancel', handler.cancel), CommandHandler('confirm', handler.confirmation)],
    )

    application.add_handler(CallbackQueryHandler(handler.button_callback_handler))
    # Add the conversation handler to the application
    application.add_handler(conv_handler)

    # Add other handlers for independent commands
    application.add_handler(CommandHandler('start', handler.start))
    application.add_handler(CommandHandler('mystats', handler.mystats))
    application.add_handler(CommandHandler('leaderboard', handler.leaderboard))
    application.add_handler(CommandHandler('invite', handler.referral))
    application.add_handler(CommandHandler('help', handler.help_command))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
