from telegram import Update
from telegram.ext import ContextTypes

from text import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.chat.id)
    await update.message.reply_text(str(update.message.chat_id))

