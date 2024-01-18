from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Для авторизации в боте перейдите по ссылке: http://localhost:80?family_id={update.message.chat_id}")
