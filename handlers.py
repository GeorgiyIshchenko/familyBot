from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

import settings

from database import *
from utils import *

host_url = "http://127.0.0.1:80" if settings.DEBUG else "ttps://notion-auth.vercel.app"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    family_id = update.message.chat_id
    auth_url = f"{host_url}/?family_id={family_id}"
    keyboard = [[InlineKeyboardButton("🟢 Авторизоваться в Notion 🟢", url=auth_url)]]
    await update.message.reply_text(
        f"👋 Приветствую! 👋\n\n👨‍👩‍👧‍👦 Рад приветсвовать тебя в нашем боте для отслеживания важных дат вашей семьи! 📅\n\n"
        f"⬇️ Для загрузки данных нажмите на кнопку ⬇️", reply_markup=InlineKeyboardMarkup(keyboard))


async def update_events(update: Update, context: ContextTypes.DEFAULT_TYPE, pre_message: str = ""):
    # TODO: update function
    update_url = f"{host_url}/events?{update.message.chat_id}"
    keyboard = [[InlineKeyboardButton(text="🟢 Обновить данные из Notion 🟢", url=f"{update_url}")]]
    await update.message.reply_text(f"{pre_message}⬇️ Нажмите кнопку чтобы обновить даты ⬇️",
                                    reply_markup=InlineKeyboardMarkup(keyboard))


async def get_family_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    family_id = update.message.chat_id
    db = SessionLocal()
    events = get_events_by_family(family_id, db)
    if events:
        result = "👨‍👩‍👧‍👦 Отлично, вот значимые события вашей семьи 📅"
        for event in events:
            result += f"{event.as_pretty_string()}\n"
        await update.message.reply_text(result, parse_mode='HTML')
    else:
        await update_events(update, context, "🔴 Вы еще не добавили ни одного события 🔴\n\n")
