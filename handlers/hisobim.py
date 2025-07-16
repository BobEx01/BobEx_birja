# handlers/hisobim.py

from telegram import Update
from telegram.ext import ContextTypes
from database import cursor
from handlers.start import asosiy_menu

async def hisobim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    balans = result[0] if result else 0

    text = f"💳 Hisobingiz: {balans} so'm\n\nTo‘lovlar faqat xizmatlar uchun ishlatiladi va qaytarilmaydi."
    await update.message.reply_text(text, reply_markup=asosiy_menu())
