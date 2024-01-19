from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import settings

from database import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    host_url = "http://127.0.0.1:80" if settings.DEBUG else "ttps://notion-auth.vercel.app"
    auth_url = f"{host_url}/?family_id={update.message.chat_id}"
    keyboard = [[InlineKeyboardButton("Авторизоваться в Notion", url=auth_url)]]
    await update.message.reply_text(
        f"Для загрузки данных нажмите на кнопку", reply_markup=InlineKeyboardMarkup(keyboard))


async def get_family_events(update: Update, context: ContextTypes):
    family_id = update.message.chat_id
    db = SessionLocal()
    result = str()
    for event in get_events_by_family(family_id, db):
        result += f"{str(event)}\n"
    await update.message.reply_text(result, parse_mode='HTML')
