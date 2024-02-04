from datetime import datetime

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from sqlalchemy import and_, func

from database import SessionLocal
from models import Event


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
    years_left = int(datetime.now().year - event.date.year)
    return f"⏰ Спешим Вас уведомить ⏰️\n\nСегодня, {event.date.day} {get_month_translation(event.date.month)}, {years_left} {get_year_translation(years_left)} назад произошло событие:\n\"{event.name}\"."


async def send_event_notifications(context: ContextTypes.DEFAULT_TYPE) -> None:
    for event in get_today_events():
        try:
            await context.application.bot.sendMessage(chat_id=event.family_id,
                                                      text=get_pretty_message(event),
                                                      parse_mode=ParseMode.HTML)
        except Exception as e:
            print(e)
