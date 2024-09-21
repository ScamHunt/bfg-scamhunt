from enum import Enum, auto
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dataclasses import dataclass

OnboardingStates = {
    "WELCOME": "welcome",
    "STEP1": "onboarding_step1",
    "STEP2": "onboarding_step2",
    "STEP3_YES": "onboarding_step3_yes",
    "STEP3_NO": "onboarding_step3_no",
    "STEP4": "onboarding_step4",
    "STEP5": "onboarding_step5",
    "STEP6": "onboarding_step6",
    "END": "onboarding_end",
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
            OnboardingStates["WELCOME"]: OnboardingMessage(
                text=(
                    "Welcome to ScamHunt! 🕵️‍♀️\n\n"
                    "We're on a mission to make Singapore safer from online scams.\n\n"
                    "Ready to join the hunt?"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Let's go!", callback_data=OnboardingStates["STEP1"]
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["STEP1"]: OnboardingMessage(
                text=(
                    "Great! Before we start, let's quickly go through how this works and what to expect.\n\n"
                    "It'll only take a minute.\n\n"
                    "Ready?"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yes, I'm ready",
                                callback_data=OnboardingStates["STEP2"],
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["STEP2"]: OnboardingMessage(
                text="First, have you ever reported suspicious posts or links on Facebook or Instagram before?",
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yes", callback_data=OnboardingStates["STEP3_YES"]
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "No", callback_data=OnboardingStates["STEP3_NO"]
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["STEP3_YES"]: OnboardingMessage(
                text=(
                    "Excellent!\n\n"
                    "Your experience will be valuable. 👍\n\n"
                    "Now, what do you think happens when a scam is reported on these platforms?"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Taken down immediately, right?",
                                callback_data=OnboardingStates["STEP4"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Platforms review it and take it down",
                                callback_data=OnboardingStates["STEP4"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "I'm not sure", callback_data=OnboardingStates["STEP4"]
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["STEP3_NO"]: OnboardingMessage(
                text=(
                    "That's ok! 👍\n\n"
                    "Now, say you did report it, what do you think happens when a scam is reported on these platforms?"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Taken down immediately, right?",
                                callback_data=OnboardingStates["STEP4"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Platforms review it and take it down",
                                callback_data=OnboardingStates["STEP4"],
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "I'm not sure", callback_data=OnboardingStates["STEP4"]
                            )
                        ],
                    ]
                ),
            ),
            OnboardingStates["STEP4"]: OnboardingMessage(
                text=(
                    "Actually, reporting doesn't guarantee removal. 😕\n\n"
                    "Platforms may review reports, but their policies aren't consistent.\n\n"
                    "⚠️ Some suspicious links may stay up even after reporting and put Singaporeans at risk."
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Really? Tell me more",
                                callback_data=OnboardingStates["STEP5"],
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["STEP5"]: OnboardingMessage(
                text=(
                    "When users report scams on Facebook or Instagram, that information isn't shared with law enforcement. 🚔\n\n"
                    "They can't take down a post till someone reports it to them specifically, which usually only happens after there's a victim.\n\n"
                    "This creates a big blind spot. 👀"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "That's frustrating. What then?",
                                callback_data=OnboardingStates["STEP6"],
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["STEP6"]: OnboardingMessage(
                text=(
                    "🕵️‍♀️ Scamhunt is building a database of user-reported suspicious links on social media to give authorities the comprehensive visibility they currently lack.\n\n"
                    "1️⃣ It provides data to push for better platform policies and effective takedown processes. 📊\n\n"
                    "2️⃣ It informs authorities about new evolving threats. 🚨\n\n"
                    "📸 Report any suspicious posts, ads, or messages on social media by sending links or screenshots to Scamhunt bot.\n\n"
                    "Confirm a few details.\n\n"
                    "We'll do the rest.\n\n"
                    "That's it!"
                ),
                keyboard=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Got it, let's start!",
                                callback_data=OnboardingStates["END"],
                            )
                        ]
                    ]
                ),
            ),
            OnboardingStates["END"]: OnboardingMessage(
                text=(
                    "🙌 Hello hunter!\n\n"
                    "🔗 Got a suspicious Facebook or Insta link? \n"
                    "Just share directly or copy, paste and send it in chat\n\n"
                    "🖼 Got a screenshot of the post? \n"
                    "Look for the image in your photos and drop it in chat\n\n"
                    "Got both? \n"
                    "You can share both!"
                )
            ),
        }

    def get_message(self, state: str):
        return self.messages[OnboardingStates[state]]
