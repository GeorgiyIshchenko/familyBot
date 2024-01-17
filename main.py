import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler

from handlers import *
from utils import send_event_notifications

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

if __name__ == "__main__":

    # Bot Setup
    application = Application.builder().token(BOT_TOKEN).build()

    # handlers
    application.add_handler(CommandHandler("start", start))

    # ques
    application.job_queue.run_repeating(callback=send_event_notifications, interval=3)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
