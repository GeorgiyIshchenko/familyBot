from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import Depends

import database
import settings

from database import *
from utils import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    family_id = update.message.chat_id
    auth_url = f"{settings.host_url}/?family_id={family_id}"
    keyboard = [[InlineKeyboardButton("🟢 Авторизоваться в Notion 🟢", url=auth_url)]]
    await update.message.reply_text(
        f"👋 Приветствую! 👋\n\n👨‍👩‍👧‍👦 Рад приветсвовать тебя в нашем боте для отслеживания важных дат вашей семьи! 📅\n\n"
        f"⬇️ Для загрузки данных нажмите на кнопку ⬇️", reply_markup=InlineKeyboardMarkup(keyboard))


async def update_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏬ Начинаю обновление базы... ⏬")
    await update_data(update, context)


async def get_family_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    family_id = update.message.chat_id
    try:
        db = SessionLocal()
        events = get_events_by_family(family_id, db)
        if events:
            events = sorted(events, key=lambda x: x.date, reverse=True)
            result = "👨‍👩‍👧‍👦 Отлично, вот значимые события вашей семьи 📅\n\n"
            for event in events:
                result += f"{event.as_pretty_string()}\n\n"
            await update.message.reply_text(result, parse_mode='HTML')
        else:
            await update.message.reply_text(
                "🔴 Вы еще не добавили ни одного события 🔴\n\n⬇️ Используйте команду /update для того чтобы обновить данные ⬇️")
    except Exception as e:
        print(e)
