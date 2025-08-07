# handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from keyboards.menu import main_menu
from database import cursor, conn, foydalanuvchilar_soni

WELCOME = (
    "👋 Assalomu alaykum!\n"
    "Bobex yuk birjasi botiga xush kelibsiz.\n\n"
    "Bu yerda siz yuklaringiz uchun haydovchi yoki transport topishingiz mumkin, "
    "shuningdek haydovchilar o‘z xizmatlarini taklif qilishlari mumkin.\n\n"
    "📌 Pastdagi menyudan kerakli bo‘limni tanlang."
)

# START komandasi
async def boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    cursor.execute(
        "INSERT OR IGNORE INTO foydalanuvchilar (user_id, username, first_name) VALUES (?, ?, ?)",
        (user.id, user.username or "", user.first_name or "")
    )
    conn.commit()

    await update.message.reply_text(WELCOME, reply_markup=main_menu())

# Yordam bo‘limi
async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ <b>Yordam bo‘limi</b>\n\n"
        "• 📢 <b>E'lon berish</b> — Yuk yoki haydovchi e'lonini joylash\n"
        "• 📄 <b>E'lonlarni ko‘rish</b> — Kanallardagi e'lonlar ro‘yxati\n"
        "• 💳 <b>Balans</b> — Hisobingizdagi mablag‘ va operatsiyalar\n\n"
        "Har bir bosqichda '⬅️ Orqaga' tugmasi bilan oldingi bosqichga qaytishingiz mumkin."
    )
    await update.message.reply_text(text, reply_markup=main_menu(), parse_mode="HTML")

# Balans ko‘rsatish
async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    cursor.execute(
        "SELECT balans, sarflangan, toldirilgan FROM foydalanuvchilar WHERE user_id = ?",
        (uid,)
    )
    row = cursor.fetchone()
    if not row:
        bal, sarf, toldi = 0, 0, 0
    else:
        bal, sarf, toldi = row
    await update.message.reply_text(
        f"💳 Balans: {bal} so‘m\n"
        f"📉 Sarflangan: {sarf} so‘m\n"
        f"🧾 To‘langan: {toldi} so‘m",
        reply_markup=main_menu()
    )

# Kanallar ro‘yxati
async def show_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📄 <b>E'lonlar kanallari</b>\n\n"
        "• 🚚 Yuk e'lonlari: @bobex_yuklar\n"
        "• 🚖 Haydovchilar: @bobex_shofyorlar\n"
        "• 📦 Umumiy: @bobex_logistika\n\n"
        "Kanallar orqali ham e'lonlaringizni joylashtirish mumkin."
    )
    await update.message.reply_text(text, reply_markup=main_menu(), parse_mode="HTML")

# Foydalanuvchilar soni
async def foydalanuvchilar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    soni = foydalanuvchilar_soni()
    await update.message.reply_text(f"📊 Foydalanuvchilar soni: {soni} ta")

# Hammasini ro‘yxatdan o‘tkazish uchun
def register_start_handlers(app):
    app.add_handler(CommandHandler("start", boshlash))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Yordam$"), show_help))
    app.add_handler(MessageHandler(filters.Regex("^💳 Balans$"), show_balance))
    app.add_handler(MessageHandler(filters.Regex("^📄 E'lonlarni ko'rish$"), show_channels))
    app.add_handler(CommandHandler("foydalanuvchilar", foydalanuvchilar_cmd))
    app.add_handler(MessageHandler(filters.Regex("^📊 Foydalanuvchilar soni$"), foydalanuvchilar_cmd))
