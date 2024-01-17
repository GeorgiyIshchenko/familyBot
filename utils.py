from datetime import datetime
from typing import Type

from fastapi import Depends
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from database import SessionLocal
from models import Event


def get_today_events() -> list[Type[Event]]:
    today_date = datetime.today().strftime('%Y-%m-%d')
    db = SessionLocal()
    return db.query(Event).filter(Event.date == today_date).all()


async def send_event_notifications(context: ContextTypes.DEFAULT_TYPE) -> None:
    for event in get_today_events():
        try:
            await context.application.bot.sendMessage(chat_id=event.family_id,
                                                      text=f"{event.name} {event.date} {event.description}",
                                                      parse_mode=ParseMode.HTML)
        except Exception as e:
            print(e)
