from dataclasses import dataclass


@dataclass
class ScamHuntMessages:
    start_message: str = (
        "🚨 Press the button below to send us suspicious social media links or screenshots \n\n"
        "See you in the hunt!"
    )

    new_scam_report: str = (
        "🙌 Hello hunter!\n\n"
        "🖼 Send us the link or screenshot of the suspicious post\n\n"
        "👯‍ Feel free to share both!"
    )

    link_sharing: str = "🚀 Ready to report this link as a potential scam?"

    phone_number_sharing: str = (
        "📞 *Thanks for sharing this phone number(s): <phone_number> !*🔍\n\n"
        "This number will be shared with ScamShield. \n"
        "If you haven't installed ScamShield yet, please visit https://www.scamshield.gov.sg for more information."
    )

    screenshot_sharing: str = "Ready to report this post as a potential scam?"

    looking_into_scam: str = (
        "🕵️ I’m looking into it...\n\n" "Please wait, this may take a few moments."
    )

    help: str = (
        "Singaporeans are losing $1 Million a week to social media scammers. Scamhunt is trying to stop them. \n\n"
        "🚨 Use /hunt or /report to send us suspicious social media links or screenshots.\n\n"
        "See you in the hunt!"
    )

    error: str = "🚫 Error! Please try again."

    scam_type: str = (
        "🙏 *Thank you for sharing a <platform> screenshot\n\n"
        "We're looking into this potential Facebook scam. Your report helps keep others safe!"
    )

    cancel: str = "🚫 *Cancelled!* If you need help, use /help or /start"

    confirm: str = (
        "🎉 Great job, hunter! \n\n"
        "Your report has been received. It will be analyzed and added to the database.\n\n"
        "Remember,\n"
        "🕵️‍♂️ If you spot a suspicious post, don’t just ignore it — report it!"
    )

    end_message: str = (
        "\n\nFeel free to report more scams with /report or /hunt. Let's keep going! 💪"
    )

    learn: str = (
        "🎓 *Want to learn more about scams?*\n\n"
        "Visit https://t.me/ncpcscamalert for regular updates about scams in Singapore and different scam types.\n\n"
        "Stay informed to stay safe! 🛡️"
    )
    
    not_a_screenshot_message: str = (
        "Oops! 🙈 It looks like this isn't a screenshot or we couldn't identify the platform.\n\nPlease try again."
    )

    def get_screenshot_result_message(scam_likelihood, reasoning):
        return (
            f"{'🚨 Very likely a scam' if scam_likelihood > 80 else '🔶 Not very likely a scam'}\n"
            f"{'Exercise extreme caution and avoid engaging further.' if scam_likelihood > 80 else 'However, please remain cautious and use your best judgment.'}\n\n"
            "🙏🏽 Please note: Our analysis system is still in testing, so results may not be 100% accurate.\n\n"
            f"*Reasoning:*\n{reasoning}\n\n"
            "Did we get it right?"
        )

    def get_screenshot_confirmation_message(scam_likelihood, similar):
        return (
            f"🎉 *Great job, hunter!*\n"
            f"{'Thank you for hunting this down.' if scam_likelihood > 80 else 'False alarm, but great instincts!'}\n\n"
            f"{'🚨 This is very likely a scam.' if scam_likelihood > 80 else '🔶 This is not likely a scam.'}\n\n"
            f"🔍 We've found {len(similar)} similar scams in our Database!\n\n"
            "Remember,\n"
            "🕵️ If you spot a suspicious post, don't just ignore it — report it!\n"
            "Let's keep going! 💪"
        )
