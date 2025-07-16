from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.utils import asosiy_menu

# /start komandasi uchun funksiya
async def boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum, BobEx botiga xush kelibsiz!\n\n"
        "Quyidagi menyulardan birini tanlang:\n\n"
        "🚛 Yuk uchun e'lon berish\n"
        "🚚 Shofyor e'lon berish\n"
        "📦 Yuk e'lonlarini ko‘rish\n"
        "🚚 Shofyor e'lonlarini ko‘rish\n"
        "💳 Hisobim — balans va hisob to‘ldirish\n"
        "🎁 Paketlar — VIP tarif va bonus paketlar",
        reply_markup=asosiy_menu()
    )
