from .supabase import supabase
from postgrest import APIError
import logging
from .report import Report
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

logging.basicConfig(level=logging.INFO)


class Feedback:
    def __init__(self, score: int = None, feature: str = None, score_why: str = None):
        self.score = score
        self.score_why = score_why
        self.feature = feature

    def to_dict(self):
        return {
            "score": self.score,
            "feature": self.feature,
            "score_why": self.score_why,
        }


class User:
    def __init__(
        self,
        id: int,
        username: str,
        first_name: str,
        last_name: str,
        feedback: Feedback = None,
    ):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.feedback = Feedback()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            feedback=Feedback(
                score=data["score_feedback"],
                feature=data["feature_feedback"],
                score_why=data["score_why"],
            ),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "score_feedback": self.feedback.score,
            "feature_feedback": self.feedback.feature,
            "score_why": self.feedback.score_why,
        }


def create_user(user: User) -> (User, Exception):
    new = user.to_dict()
    try:
        data = supabase.table("user").insert(new).execute()
        return (data.data[0], None)
    except APIError as e:
        logging.error(f"Error creating user: {e}")


def get_user(id: int) -> (User | None, Exception | None):
    try:
        data = supabase.table("user").select("*").eq("id", id).limit(1).execute()
        if not data.data:
            return (None, None)
        user_data = data.data[0]
        return (User.from_dict(user_data), None)
    except APIError as e:
        logging.error(f"Error getting user: {e}")
        return (None, e)


def get_user_reports(id: int) -> (list[Report], Exception):
    try:
        data = supabase.table("report").select("*").in_("user_id", [id]).execute()
        return (data.data, None)
    except APIError as e:
        logging.error(f"Error getting user reports: {e}")
        return (None, e)


def update_user_feedback(id: int, feedback: Feedback) -> (User, Exception):
    try:
        data = (
            supabase.table("user")
            .update(
                {
                    "score_feedback": feedback.score,
                    "feature_feedback": feedback.feature,
                    "score_why": feedback.score_why,
                }
            )
            .eq("id", id)
            .execute()
        )
        return (data.data[0], None)
    except APIError as e:
        logging.error(f"Error updating user feedback: {e}")
        return (None, e)


def create_user_if_not_exists(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Creating user if not exists for {update.effective_user.id}")
    user, _ = get_user(update.effective_user.id)
    if user is None:
        user = User(
            id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
        )
        create_user(user)
        context.user_data["is_new"] = True
        logging.info(f"New user: {user}")
    else:
        context.user_data["is_new"] = False


def get_banned_users() -> (list[int], Exception):
    try:
        data = supabase.table("user").select("id").eq("is_banned", True).execute()
        logging.info(f"Banned users: {[user["id"] for user in data.data]}")
        return ([user["id"] for user in data.data], None)
    except APIError as e:
        logging.error(f"Error getting banned users: {e}")
        return (None, e)


def is_banned(func):
    @wraps(func)
    async def wrapper(update, context):
        userid = (
            update.message.from_user.id
            if update.message
            else update.callback_query.from_user.id
        )
        banned_users, _ = get_banned_users()
        if not userid in banned_users:
            await func(update, context)
        else:
            response = (
                "`💀 Account suspended\n"
                "We take the safety and integrity of our community seriously.\n\n"
                "Thank you for your understanding.`"
            )
            if update.message:
                await update.message.reply_text(response, parse_mode="Markdown")
            elif update.callback_query:
                await update.callback_query.answer(response, show_alert=True)

    return wrapper
