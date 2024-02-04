from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

import database
import settings
import requests

from database import *
from utils import *

host_url = "http://127.0.0.1:80" if settings.DEBUG else "https://notion-auth.vercel.app"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    family_id = update.message.chat_id
    print(update.message.chat, family_id)
    auth_url = f"{host_url}/?family_id={family_id}"
    keyboard = [[InlineKeyboardButton("🟢 Авторизоваться в Notion 🟢", url=auth_url)]]
    await update.message.reply_text(
        f"👋 Приветствую! 👋\n\n👨‍👩‍👧‍👦 Рад приветсвовать тебя в нашем боте для отслеживания важных дат вашей семьи! 📅\n\n"
        f"⬇️ Для загрузки данных нажмите на кнопку ⬇️", reply_markup=InlineKeyboardMarkup(keyboard))


async def update_events(update: Update, context: ContextTypes.DEFAULT_TYPE, pre_message: str = ""):
    # TODO: update function
    update_url = f"{host_url}/events"

    try:
        db = SessionLocal()
        family = get_family_by_id(update.message.chat_id, db)

        req = requests.get(url=update_url, json={"family_id": family.family_id, "access_token": family.access_token})

        for event in get_events_by_family(family.family_id, db):
            db.delete(event)

        for event in req.json()["events"]:
            create_event(name=event["name"], date=datetime.strptime(event["date"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                         description=event["description"],
                         family_id=event["family_id"], db=db)

        db.commit()

        await update.message.reply_text(f"🟢 Обновление прошло успешно! 🟢")
    except Exception as e:
        print(e)
        await update.message.reply_text("🔴 Что-то пошло не так! 🔴")


async def get_family_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    family_id = update.message.chat_id
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
