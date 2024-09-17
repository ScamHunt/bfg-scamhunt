import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import os
from dotenv import load_dotenv
# from bot.link.response import handle_link
import bot.handler as handler


load_dotenv('.env', override=True) 
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
application = ApplicationBuilder().token(bot_token).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("report", handler.handle_report)],
    states={
        handler.REPORT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_report_type)],
        handler.DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_report_details)],
        handler.CONFIRMATION: [CommandHandler("confirm", handler.handle_report_confirmation)],
    },
    fallbacks=[CommandHandler("cancel", handler.cancel)],
)


def main():    
    # Command Handlers
    application.add_handler(CommandHandler("start", handler.start))
    application.add_handler(CommandHandler("menu", handler.menu))
    application.add_handler(CommandHandler("info", handler.info))
    application.add_handler(CommandHandler("stats", handler.stats))
    application.add_handler(CommandHandler("help", handler.help))
    # Conversation Handlers
    application.add_handler(conv_handler)
    # Message Handlers
    application.add_handler(MessageHandler(filters.ATTACHMENT, handler.handle_attachment))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_general))
    application.add_error_handler(handler.error_handler)
    # Run the bot
    application.run_polling()
