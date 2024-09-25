from .supabase import supabase
from postgrest import APIError
import logging
from .report import Report
from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(level=logging.INFO)

class Feedback:
    def __init__(self, score: int = None, feature: str = None):
        self.score = score
        self.feature = feature

    def to_dict(self):
        return {
            "score": self.score,
            "feature": self.feature,
        }


class User:
    def __init__(self, id: int, username: str, first_name: str, last_name: str, feedback: Feedback = None):
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
                score=data["score_feedback"], feature=data["feature_feedback"]
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
            .update({"score_feedback": feedback.score, "feature_feedback": feedback.feature})
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
