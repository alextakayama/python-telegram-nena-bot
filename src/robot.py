from debug import Debuggable
from mailer import Mailer
from nena import Nena
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import json
import os

class TelegramBot(Debuggable):
    def __init__(self, debug: bool = False):
        super().__init__(debug)
        self.allowed_user_ids = os.getenv("ALLOWED_USER_IDS").split(",")
        self.mailer = Mailer(debug)
        self.nena = Nena(debug)
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")

    async def delete_command(self, update: Update, context):
        """Delete message from the mailbox"""
        if not context.args:
            await update.message.reply_text("Please provide a message number. Example: /delete 3")
            return

        msg_id = context.args[0].encode('ascii')

        self.mailer.delete_message(msg_id)

        await update.message.reply_text("The message has been removed.")

    async def error_handler(self, update: Update, context):
        """Because sometimes things go sideways..."""
        self.log_debug(f"Update {update} caused error {context.error}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

    async def handle_message(self, update: Update, context):
        """Receive message from user and respond"""
        user = update.effective_user
        self.log_debug(f"User = {user}")

        user_message = update.message
        self.log_debug(f"Message = {user_message}")

        user_id = str(user.id)

        if user_id not in self.allowed_user_ids:
            self.log_warning(f"USER IS BLOCKED = {user}")
            await update.message.reply_text("Sorry, I don't talk to strangers...")
            return

        response_text = self.nena.ask_me(user_id, user_message.text)

        self.log_debug(f"LLM -> {user.username} = {response_text}")

        await update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)

    async def list_command(self, update: Update, context):
        """List messages from the mailbox"""
        all = True

        if len(context.args) > 0:
            if context.args[0] == "unread":
                all = False

        count = 0
        response_text = ""

        for email_message in self.mailer.list_inbox_messages(all):
            response_text += email_message.get("Id").decode("ascii") + ") " 
            response_text += email_message.get("Subject") + " \n"
            response_text += "From: " + email_message.get("From") + " \n"
            response_text += "Date: " + email_message.get("Date") + " \n\n"
            count = count + 1

        if count < 1:
            response_text = "You have no messages in your mailbox."
        else:
            response_text = "You have " + str(count) + " message(s) in your mailbox. \n\n" + response_text

        await update.message.reply_text(response_text)

    async def read_command(self, update: Update, context):
        """Read a message in the mailbox"""
        if not context.args:
            await update.message.reply_text("Please provide a message number. Example: /read 4")
            return

        msg_id = context.args[0].encode('ascii')

        email_message = self.mailer.read_message(msg_id)
        if email_message is None:
            await update.message.reply_text("I can't find your message.")
            return

        response_text  = email_message.get("Id").decode("ascii") + ") " 
        response_text += email_message.get("Subject") + " \n"
        response_text += "From: " + email_message.get("From") + " \n"
        response_text += "Date: " + email_message.get("Date") + " \n\n"
        response_text += email_message.get("Body")

        await update.message.reply_text(response_text)

    async def start_command(self, update: Update, context):
        """Start a conversation"""
        await update.message.reply_text("Hi there! 😊 I'm Nena, here to help and make things easier for you. Let me know what you need, and I'll do my best to assist. Looking forward to helping you!")

    async def summarize_command(self, update: Update, context):
        """Summarize a message in the mailbox"""
        if not context.args:
            await update.message.reply_text("Please provide a message number. Example: /summarize 5")
            return

        msg_id = context.args[0].encode('ascii')

        email_message = self.mailer.read_message(msg_id)
        if email_message is None:
            await update.message.reply_text("I can't find your message.")
            return

        email_message['Id'] = email_message['Id'].decode('ascii')

        user = update.effective_user
        self.log_debug(f"User = {user}")

        user_id = str(user.id)

        if user_id not in self.allowed_user_ids:
            self.log_warning(f"USER IS BLOCKED = {user}")
            await update.message.reply_text("Sorry, I don't talk to strangers...")
            return

        prompt  = "Consider the following JSON object that represents an email: \n\n"
        prompt += json.dumps(email_message) + " \n\n"
        prompt += "Please provide a concise summary of its content (2-3 sententes), including who sent it, the subject, the date, and the main idea of the message body. \n"
        prompt += "Keep the JSON technical details out of your response. "

        response_text = self.nena.ask_me(user_id, prompt)

        self.log_debug(f"LLM -> {user.username} = {response_text}")

        await update.message.reply_text(response_text)

    def startup(self) -> None:
        # Create the application
        application = Application.builder().token(self.telegram_token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("list", self.list_command))
        application.add_handler(CommandHandler("read", self.read_command))
        application.add_handler(CommandHandler("delete", self.delete_command))
        application.add_handler(CommandHandler("summarize", self.summarize_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Add error handlers
        application.add_error_handler(self.error_handler)

        self.log_debug("Starting Telegram Bot")

        # Start the bot
        application.run_polling()
