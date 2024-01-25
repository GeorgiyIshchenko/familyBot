import asyncio
import os
import uvicorn

from dotenv import load_dotenv

from telegram.ext import Application, CommandHandler

from api import app
from handlers import *
from utils import send_event_notifications

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

if __name__ == "__main__":
    # Bot Setup
    application = Application.builder().token(BOT_TOKEN).build()
    # handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("events", get_family_events))
    application.add_handler(CommandHandler("update", update_events))
    # ques
    application.job_queue.run_repeating(callback=send_event_notifications, interval=300)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
