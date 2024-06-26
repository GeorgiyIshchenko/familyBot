import os

from dotenv import load_dotenv
from datetime import time
from telegram.ext import Application, CommandHandler

from handlers import *
from utils import send_event_notifications

import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

if __name__ == "__main__":
    # Bot Setup
    application = Application.builder().token(BOT_TOKEN).read_timeout(40).get_updates_read_timeout(40).connect_timeout(
        40).write_timeout(40).get_updates_connect_timeout(40).pool_timeout(40).build()
    # handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("events", get_family_events))
    application.add_handler(CommandHandler("update", update_events))
    # ques
    application.job_queue.run_once(callback=send_event_notifications, when=1)
    application.job_queue.run_daily(callback=send_event_notifications, time=time(hour=6))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
