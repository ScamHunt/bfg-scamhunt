class ScamHuntMessages:
    def __init__(self):
        # Version 1 Messages

        self.start_message = (
            "🚨 Press the button below to send us suspicious social media links or screenshots \n\n"
            "See you in the hunt!"
        )

        self.new_scam_report = (
            "🙌 Hello hunter!\n\n"
            "🔗 Got a suspicious Facebook or Insta link? \n"
            "Just share directly or copy, paste and send it in chat\n\n"
            "🖼 Got a screenshot of the post? \n"
            "Look for the image in your photos and drop it in chat\n\n"
            "Got both? \n"
            "You can share both!"
        )

        # Shared scam with us Messages
        self.link_sharing = "🚀 Thanks for sharing this <link> scam! I'm checking out that link right now... 🔍\n\n"

        self.phone_number_sharing = (
            "📞 *Thanks for sharing this phone number(s): <phone_number> !*🔍\n\n"
            "This number will be added to ScamShield database. \n"
            "If you haven't installed ScamShield yet, please visit https://www.scamshield.gov.sg for more information."
        )

        self.screenshot_sharing = (
            "🖼️ Thanks for sharing a *suspicious screenshot!*\n\n"
            "Could you confirm if this is the screenshot of the suspicious post you're reporting?"
        )

        self.looking_into_scam = (
            "🔍 I'm looking into this. Please wait a moment... \n\n"
        )

        self.text_sharing = (
            "📝 *Thanks for sharing a scam text!* I'm taking a look... 🔍\n\n"
            "Was this a message you received?"
        )

        # Scam about messages
        self.ask_scam_about = (
            "Want to share more details? Use /scamabout to add more info! 📝\n\n"
            "Send /cancel to stop the conversation\n"
            "Send /confirm to confirm the scam report."
        )
        self.press_scam_about = (
            "📢 *Please share any screenshots or details about the scam in this chat* 📸\n\n"
            "Send /cancel to stop the conversation\n"
            "Send /confirm to confirm the scam report."
        )

        # Scam about follow up messages
        self.screenshot_followup = (
            "*Did you know?* Adding links makes us 30% more effective in taking down scams! 🛡️\n"
            "Use /scamlink to add a link!"
        )

        # Other messages
        self.encouragement = (
            "⏰ *It's been a while since your last hunt!* Remember, ignoring a scam only protects you—"
            "reporting it protects everyone! 🔒 Use /report to jump back in! 💼"
        )

        self.help = (
            "Singaporeans are losing $1 Million a week to social media scammers. Scamhunt is trying stop them. \n\n"
            "🚨 /hunt or /report to send us suspicious social media links or screenshots \n"
            "📊 /myhunt to view your contributions and scams you've stopped \n"
            "💪 /huntprogress tosee how to level up \n"
            "🏆 /scamhunters to see the top Scam Hunters in Singapore\n\n"
            "Send us a suspicious link directly or /hunt to start sharing?\n\n"
            "See you in the hunt!"
        )
        self.leadership = (
            "🏅 *Awesome job!* You've reported 5 scams this week! 🏆\n\n"
            "You're in the top 10% of scam hunters! Keep going and climb the ranks! 💪"
        )

        self.error = "🚫 *Error!* Please try again. If the problem persists, contact @scamhuntbot"

        # Scam types
        self.scam_type = (
            "🙏 *Thank you for sharing a <platform> screenshot\n\n"
            "We're looking into this potential Facebook scam. Your report helps keep others safe!"
        )

        self.cancel = "🚫 *Cancelled!* If you need help, use /help or /start"
        self.confirm = (
            "🎉 *Confirmed!* Thanks for keeping Singapore safe from scams! 🙌"
        )
        self.end_message = "\n\nFeel free to report more scams with /report or /hunt. Let's keep going! 💪"
        # Learn messages
        self.learn = (
            "🎓 *Want to learn more about scams?*\n\n"
            "Visit https://t.me/ncpcscamalert for regular updates about scams in Singapore and different scam types.\n\n"
            "Stay informed to stay safe! 🛡️"
        )
