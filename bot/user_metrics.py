from amplitude import Amplitude, BaseEvent
import os
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import logging

amplitude_logger = logging.getLogger("amplitude")
amplitude_logger.setLevel(logging.DEBUG)
amplitude = Amplitude(api_key=os.getenv("AMPLITUDE_API_KEY"))


class Event(BaseEvent):
    def __init__(self, user_id, event_name):
        self.user_id = user_id
        self.event_name = event_name


def track_user_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    event_type = update.callback_query.data.replace("_", " ").title() if update.callback_query and update.callback_query.data else "Unknown Event"
    amplitude.track(
        BaseEvent(
            user_id=str(update.effective_user.id),
            event_type=event_type,
            user_properties={
                "chat_id": update.effective_chat.id,
                "message_id": update.effective_message.message_id,
                "username": update.effective_user.username,
                "first_name": update.effective_user.first_name,
                "last_name": update.effective_user.last_name,
                "language_code": update.effective_user.language_code,
                "is_bot": update.effective_user.is_bot,
            },
            time=int(datetime.now().timestamp() * 1000),
            platform="telegram",
        )
    )
    
    amplitude.flush()
