from datetime import datetime

import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from sqlalchemy import and_, func

from database import *
from models import Event

import settings


def get_today_events() -> list[Event]:
    today_date = datetime.today()
    db = SessionLocal()
    events = db.query(Event).all()
    result = list()
    for event in events:
        if event.date.month == today_date.month and event.date.day == today_date.day:
            result.append(event)
    return result


def get_year_translation(year: int) -> str:
    return "год" if 1 <= year % 10 <= 4 else "лет"


def get_month_translation(month: int) -> str:
    return ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
            'декабря')[month - 1]


def get_pretty_message(event: Event):
    return f"⏰ Спешим Вас уведомить ⏰️\n\n{event.date.day} {get_month_translation(event.date.month)} {event.date.year} году произошло событие:\n\"{event.name}\"."


async def send_event_notifications(context: ContextTypes.DEFAULT_TYPE) -> None:
    for event in get_today_events():
        try:
            await context.application.bot.sendMessage(chat_id=event.family_id,
                                                      text=get_pretty_message(event),
                                                      parse_mode=ParseMode.HTML)
        except Exception as e:
            print(e)


async def update_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_url = f"{settings.host_url}/events"

    try:
        db = SessionLocal()
        family = get_family_by_id(update.message.chat_id, db)
        req = requests.get(url=update_url, json={"family_id": family.family_id, "access_token": family.access_token},
                           timeout=10)

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
