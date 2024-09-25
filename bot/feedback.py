from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.handler.callbacks import CallbackData
from bot.db.user import update_user_feedback, Feedback
from typing import Dict, Union


class FeedbackStates:
    FEEDBACK_SCORE = "feedback_score"
    FEEDBACK_SCORE_WHY = "feedback_score_why"
    FEEDBACK_ADDITIONAL_FEATURE = "feedback_additional_feature"
    FEEDBACK_END = "feedback_end"


class FeedbackMessage:
    def __init__(self, text: str, keyboard: InlineKeyboardMarkup = None):
        self.text = text
        self.keyboard = keyboard


class FeedbackMessages:
    def __init__(self):
        self.feature_options = [
            "My personal reporting stats",
            "A dedicated page for my reports",
            "Gamification (e.g., badges, leaderboard)",
            "Scam simulation exercises",
            "Status of my reported links",
            "None, it's good as it is",
        ]
        self.why_options = [
            "Bot is too complicated to use",
            "Don't see suspicious posts frequently",
            "I don't know what happens next",
            "Not confident in my ability to identify scams",
            "I forget this bot exists",
        ]
        self.messages: Dict[str, FeedbackMessage] = {
            FeedbackStates.FEEDBACK_SCORE: self._create_score_message(),
            FeedbackStates.FEEDBACK_SCORE_WHY: self._create_score_why_message(),
            FeedbackStates.FEEDBACK_ADDITIONAL_FEATURE: self._create_feature_message(),
            FeedbackStates.FEEDBACK_END: self._create_end_message(),
        }

    def _create_score_message(self) -> FeedbackMessage:
        buttons = [
            [
                InlineKeyboardButton(
                    str(i),
                    callback_data=f"{FeedbackStates.FEEDBACK_SCORE_WHY}:{i}",
                )
                for i in range(1, 4)
            ]
            + [
                InlineKeyboardButton(
                    "4",
                    callback_data=f"{FeedbackStates.FEEDBACK_ADDITIONAL_FEATURE}:4",
                ),
                InlineKeyboardButton(
                    "5",
                    callback_data=f"{FeedbackStates.FEEDBACK_ADDITIONAL_FEATURE}:5",
                ),
            ]
        ]
        return FeedbackMessage(
            text="How likely are you to use this bot again for reporting scams?",
            keyboard=InlineKeyboardMarkup(buttons),
        )

    def _create_score_why_message(self) -> FeedbackMessage:
        return FeedbackMessage(
            text="Could you tell us why you chose that score?",
            keyboard=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            option,
                            callback_data=f"{FeedbackStates.FEEDBACK_ADDITIONAL_FEATURE}:{i+1}",
                        )
                    ]
                    for i, option in enumerate(self.why_options)
                ]
            ),
        )

    def _create_feature_message(self) -> FeedbackMessage:
        return FeedbackMessage(
            text="Choose 1: What additional feature would you like to see the most in the bot?",
            keyboard=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            feature,
                            callback_data=f"{FeedbackStates.FEEDBACK_END}:{i+1}",
                        )
                    ]
                    for i, feature in enumerate(self.feature_options)
                ]
            ),
        )

    def _create_end_message(self) -> FeedbackMessage:
        return FeedbackMessage(
            text=(
                "🎉 Thank you, hunter!\n\n"
                "If you have any more suggestions or encounter any issues, use the /feedback command to share anytime. "
                "Thank you again for being an active member of our anti-scam community!\n\n"
                "🕵️ If you spot a suspicious link, don't just ignore it — report it!"
            ),
            keyboard=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Hunt on Facebook",
                            url="https://www.facebook.com/report.scam",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Hunt on Instagram",
                            url="https://www.instagram.com/report.scam",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Report suspicious post",
                            callback_data=CallbackData.REPORT_SCAM,
                        )
                    ],
                ]
            ),
        )

    def get_message(self, state: str) -> Union[FeedbackMessage, str]:
        return self.messages.get(state, "Invalid state")

    def get_state(self, data: str, context: ContextTypes.DEFAULT_TYPE) -> str:
        parts = data.split(":")
        state = parts[0]
        if state == FeedbackStates.FEEDBACK_SCORE:
            return state
        elif state == FeedbackStates.FEEDBACK_SCORE_WHY:
            context.user_data["score"] = int(parts[1])
            return state
        elif state == FeedbackStates.FEEDBACK_ADDITIONAL_FEATURE:
            if "score" not in context.user_data:
                context.user_data["score"] = int(parts[1])
            if "score_why" not in context.user_data:
                context.user_data["score_why"] = self.why_options[int(parts[1]) - 1]
            return state
        elif state == FeedbackStates.FEEDBACK_END:
            context.user_data["feature"] = self.feature_options[int(parts[1]) - 1]
            return state
        return None


feedback_messages = FeedbackMessages()


async def process_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    state = feedback_messages.get_state(query.data, context)
    if state == FeedbackStates.FEEDBACK_END:
        score_why = None
        if "score_why" in context.user_data:
            score_why = context.user_data["score_why"]
        user_feedback = Feedback(
            score=context.user_data["score"],
            feature=context.user_data["feature"],
            score_why=score_why,
        )
        update_user_feedback(update.effective_user.id, user_feedback)
        context.user_data["is_new"] = False
    message = feedback_messages.get_message(state=state)
    await query.edit_message_text(text=message.text, reply_markup=message.keyboard)


def is_feedback(data: str) -> bool:
    return (
        data.startswith(FeedbackStates.FEEDBACK_SCORE)
        or data.startswith(FeedbackStates.FEEDBACK_SCORE_WHY)
        or data.startswith(FeedbackStates.FEEDBACK_ADDITIONAL_FEATURE)
        or data.startswith(FeedbackStates.FEEDBACK_END)
    )
