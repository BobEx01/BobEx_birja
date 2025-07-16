# handlers/start.py

from telegram import ReplyKeyboardMarkup
from config import ADMIN_USERNAME

def main_menu():
    keyboard = [
        ["🚛 Yuk uchun e'lon berish"],
        ["🚚 Shofyor e'lon berish"],
        ["📦 Yuk e'lonlarini ko‘rish"],
        ["🚚 Shofyor e'lonlarini ko‘rish"],
        ["💳 Hisobim", "🎟 Paketlar"],
        ["❓ Yordam"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_handler(update, context):
    await update.message.reply_text(
        "Assalomu alaykum!\n\n"
        "Quyidagi menyudan birini tanlang:",
        reply_markup=main_menu()
    )

async def help_handler(update, context):
    await update.message.reply_text(
        "Botdan foydalanish bo‘yicha yordam:\n\n"
        "👉 Yuk uchun e'lon berish: Yukingizni joylang\n"
        "👉 Shofyor e'lon berish: Transportchi sifatida e'lon bering\n"
        "👉 Yuk va Shofyor e'lonlarini ko‘rish: E'lonlarni ko‘rib, raqam olish\n"
        "👉 Hisobim: Balans, VIP, Paket\n"
        "👉 Paketlar: Maxsus chegirmali paketlar\n"
        "Yordam uchun: " + ADMIN_USERNAME,
        reply_markup=main_menu()
    )
