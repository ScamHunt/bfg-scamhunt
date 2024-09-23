from dataclasses import dataclass


@dataclass
class ScamHuntMessages:
    start_message: str = (
        "🚨 Press the button below to send us suspicious social media links or screenshots \n\n"
        "See you in the hunt!"
    )

    new_scam_report: str = (
        "🙌 Hello hunter!\n\n"
        "🔗 Got a suspicious Facebook or Insta link? \n"
        "Just share directly or copy, paste and send it in chat\n\n"
        "🖼 Got a screenshot of the post? \n"
        "Look for the image in your photos and drop it in chat\n\n"
        "Got both? \n"
        "You can share both!"
    )

    link_sharing: str = (
        "🚀 Thanks for sharing this <link> scam! I'm checking out that link right now... 🔍\n\n"
    )

    phone_number_sharing: str = (
        "📞 *Thanks for sharing this phone number(s): <phone_number> !*🔍\n\n"
        "This number will be shared with ScamShield. \n"
        "If you haven't installed ScamShield yet, please visit https://www.scamshield.gov.sg for more information."
    )

    screenshot_sharing: str = (
        "🖼️ Thanks for sharing a *suspicious screenshot!*\n\n"
        "Could you confirm if this is the screenshot of the suspicious post you're reporting?"
    )

    looking_into_scam: str = "🔍 I'm looking into this. Please wait a moment... \n\n"

    help: str = (
        "Singaporeans are losing $1 Million a week to social media scammers. Scamhunt is trying to stop them. \n\n"
        "🚨 Use /hunt or /report to send us suspicious social media links or screenshots.\n\n"
        "See you in the hunt!"
    )

    error: str = (
        "🚫 *Error!* Please try again. If the problem persists, contact @scamhuntbot"
    )

    scam_type: str = (
        "🙏 *Thank you for sharing a <platform> screenshot\n\n"
        "We're looking into this potential Facebook scam. Your report helps keep others safe!"
    )

    cancel: str = "🚫 *Cancelled!* If you need help, use /help or /start"

    confirm: str = "🎉 *Confirmed!* Thanks for keeping Singapore safe from scams! 🙌"

    end_message: str = (
        "\n\nFeel free to report more scams with /report or /hunt. Let's keep going! 💪"
    )

    learn: str = (
        "🎓 *Want to learn more about scams?*\n\n"
        "Visit https://t.me/ncpcscamalert for regular updates about scams in Singapore and different scam types.\n\n"
        "Stay informed to stay safe! 🛡️"
    )
