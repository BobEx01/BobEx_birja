from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

# Asosiy menyu funksiyasi
def asosiy_menu():
    keyboard = [
        ["🚛 Yuk uchun e'lon berish", "🚚 Shofyor e'lon berish"],
        ["📦 Yuk e'lonlarini ko‘rish", "🚚 Shofyor e'lonlarini ko‘rish"],
        ["📊 Mening hisobim", "Hisobni to‘ldirish"],
        ["🎁 Paketlar", "🗂 E'lonlarim"],
        ["💸 Pul ishlash"],
        ["📣 Admin xabar"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# /start komandasi uchun funksiya
async def boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum, BobEx botiga xush kelibsiz!\n\n"
        "Quyidagi menyulardan birini tanlang:\n\n"
        "🚛 Yuk uchun e'lon berish\n"
        "🚚 Shofyor e'lon berish\n"
        "📦 Yuk e'lonlarini ko‘rish\n"
        "🚚 Shofyor e'lonlarini ko‘rish\n"
        "📊 Mening hisobim — balans va hisob to‘ldirish\n"
        "Hisobni to‘ldirish — balansni to‘ldiring\n"
        "🎁 Paketlar — VIP tarif va bonus paketlar\n"
        "🗂 E'lonlarim — o'zingiz bergan e'lonlarni ko‘rish\n"
        "💸 Pul ishlash — do‘stlaringizni taklif qilib bonus oling\n"
        "📣 Admin xabar — admin bilan bog‘lanish",
        reply_markup=asosiy_menu()
    )
