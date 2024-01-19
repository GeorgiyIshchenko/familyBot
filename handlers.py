from telegram import Update
from telegram.ext import ContextTypes

import settings

from database import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    host_url = "http://127.0.0.1:80" if settings.DEBUG else "ttps://notion-auth.vercel.app"
    await update.message.reply_text(
        f"Для авторизации в боте перейдите по ссылке: {host_url}/?family_id={update.message.chat_id}")


async def get_family_events(update: Update, context: ContextTypes):
    family_id = update.message.chat_id
    db = SessionLocal()
    result = str()
    for event in get_events_by_family(family_id, db):
        result += f"{str(event)}\n"
    await update.message.reply_text(result, parse_mode='HTML')
