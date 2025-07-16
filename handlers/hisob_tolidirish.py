from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.start import asosiy_menu

async def hisobni_tolidirish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = (
        f"💳 *Hisobni to‘ldirish uchun karta rekvizitlari:*\n\n"
        "🔹 *Humo:* 5614 6822 1820 6250\n"
        "🔹 *Uzcard:* 8600 1234 5678 9012\n\n"
        f"🆔 *Foydalanuvchi ID:* `{user_id}`\n\n"
        "🔹 *Minimal:* 10,000 so'm\n"
        "🔹 *Maksimal:* 10,000,000 so'm\n\n"
        "*Karta egasi:* Muhammadbobur.A\n\n"
        "1️⃣ Pul o'tkazing\n"
        "2️⃣ Admin bilan bog‘laning: @admin_username\n\n"
        "_⚠️ To‘lovingiz 15-500 daqiqa ichida tekshiriladi._"
    )
    await update.message.reply_text(text, reply_markup=asosiy_menu(), parse_mode="Markdown")
