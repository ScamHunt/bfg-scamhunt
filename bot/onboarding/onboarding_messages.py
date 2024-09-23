from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.handler.callbacks import CallbackData


OnboardingStates = {
    "INTRO": "onboarding_intro",
    "REPORTED_BEFORE_YES": "onboarding_reported_before_yes",
    "REPORTED_BEFORE_NO": "onboarding_reported_before_no",
    "WHAT_HAPPENS_NEXT": "onboarding_what_happens_next",
    "REPORTING_ISSUES": "onboarding_reporting_issues",
    "SCAMHUNT_SOLUTION": "onboarding_scamhunt_solution",
    "HOW_TO_HELP": "onboarding_how_to_help",
    "END": "onboarding_end",
    "EXAMPLE_START": "example_start",
    "EXAMPLE_SHARE": "example_share",
    "EXAMPLE_WAITING": "example_waiting",
}


def get_state(value: str):
    for key, val in OnboardingStates.items():
        if val == value:
            return key
    return None  # Return None if the value is not found


class OnboardingMessage:
    def __init__(self, text: str, keyboard: InlineKeyboardMarkup = None):
        self.text = text
        self.keyboard = keyboard


class OnboardingMessages:
    def __init__(self):
        self.messages = {
            OnboardingStates["INTRO"]: OnboardingMessage(
                text="Have you ever reported suspicious posts or links on Facebook or Instagram before?",
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yes", callback_data=OnboardingStates["REPORTED_BEFORE_YES"]
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "No", callback_data=OnboardingStates["REPORTED_BEFORE_NO"]
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["REPORTED_BEFORE_YES"]: OnboardingMessage(
                text=("Excellent!\n\n" "What do you think happens next?"),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "It's taken down immediately",
                                callback_data=OnboardingStates["WHAT_HAPPENS_NEXT"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Platforms review it and take it down",
                                callback_data=OnboardingStates["WHAT_HAPPENS_NEXT"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "I'm not sure", callback_data=OnboardingStates["WHAT_HAPPENS_NEXT"]
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["REPORTED_BEFORE_NO"]: OnboardingMessage(
                text=(
                    "That's ok! 👍\n\n"
                    "Now, say you did report it, what do you think happens when a scam is reported on these platforms?"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "It's taken down immediately",
                                callback_data=OnboardingStates["WHAT_HAPPENS_NEXT"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Platforms review it and take it down",
                                callback_data=OnboardingStates["WHAT_HAPPENS_NEXT"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "I'm not sure", callback_data=OnboardingStates["WHAT_HAPPENS_NEXT"]
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["WHAT_HAPPENS_NEXT"]: OnboardingMessage(
                text=(
                    "Actually, reporting doesn't guarantee removal. 😕\n\n"
                    "Platform policies aren't consistent.\n\n"
                    "⚠️ Suspicious links stay up even after reporting.\n\n"
                    "🚔 Platforms don't proactively share suspicious links with law enforcement.\n\n"
                    "This creates a big blind spot and puts Singaporeans at risk. 👀"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Oh! How to fix this?",
                                callback_data=OnboardingStates["REPORTING_ISSUES"],
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["REPORTING_ISSUES"]: OnboardingMessage(
                text=(
                    "Scamhunt is taking the first step.\n\n"
                    "We're creating a database of suspicious social media links reported by users. This gives authorities much-needed visibility.\n\n"
                    "📊 Data to improve platform policies & takedown processes\n\n"
                    "👮‍♂️ Informs authorities about evolving threats"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Got it! How can I help?",
                                callback_data=OnboardingStates["SCAMHUNT_SOLUTION"],
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["SCAMHUNT_SOLUTION"]: OnboardingMessage(
                text=(
                    "📸 Report suspicious social media content to Scamhunt bot\n"
                    "🔗 Send links or screenshots\n"
                    "✅ Confirm details\n"
                    "🤖 We'll handle the rest!"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Try with an example",
                                callback_data=OnboardingStates["EXAMPLE_START"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Got it, let's start!",
                                callback_data=OnboardingStates["END"],
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["END"]: OnboardingMessage(
                text=(
                    "Fantastic! \n\n"
                    "Share accurate and consistent reports to:\n\n"
                    "1. 📈 Boost your rank on our leaderboard\n"
                    "2. 🏅 Unlock new achievements and titles\n\n"
                    "Remember:\n"
                    "🔍 ScamHunt provides data, not direct takedowns\n"
                    "🕵️‍♀️ When you find a real suspicious post, send a link or screenshot to this bot.\n\n"
                    "See you in the hunt! 🙌"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Report suspicious post", callback_data=CallbackData.REPORT_SCAM
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["EXAMPLE_START"]: OnboardingMessage(
                text=(
                    "Let's say you've found this post on Facebook:\n\n"
                    '"Earn $5000 daily with this secret investment trick! Limited slots available. DM now! 💰💰"\n\n'
                    "How would you report this?  🤔"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Share the post link with Scamhunt bot",
                                callback_data=OnboardingStates["EXAMPLE_SHARE"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Share a screenshot with Scamhunt bot",
                                callback_data=OnboardingStates["EXAMPLE_SHARE"],
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["EXAMPLE_SHARE"]: OnboardingMessage(
                text=(
                    "Try sharing something\n\n"
                    "📱 Open your Facebook or Instagram app\n"
                    "🔍 Find a post to share (Pick any for now)\n"
                    "🔗 Copy the link or take a screenshot\n"
                    "📤 Send it to the Scamhunt Telegram bot"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Got it. I’ll share now",
                                callback_data=OnboardingStates["EXAMPLE_WAITING"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Skip this for now",
                                callback_data=OnboardingStates["END"],
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["EXAMPLE_WAITING"]: OnboardingMessage(
                text=("Ok! Waiting for you to share..\n\n"),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Skip this for now",
                                callback_data=OnboardingStates["END"],
                            )
                        ]
                    ]
                ),
            ),
        }

    def get_message(self, state: str):
        return self.messages[OnboardingStates[state]]
