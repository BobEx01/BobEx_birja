# handlers/hisobim.py

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USERNAME

async def hisobim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"👤 Hisobingiz haqida ma'lumot:\n\n"
    text += f"🆔 ID: {user.id}\n"
    text += f"📛 Username: @{user.username}\n"
    text += f"📝 Ism: {user.first_name}\n"
    text += f"📞 Admin: {ADMIN_USERNAME}\n"
    
    await update.message.reply_text(text)
