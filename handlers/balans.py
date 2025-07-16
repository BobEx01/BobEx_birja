# handlers/balans.py

from telegram import ReplyKeyboardMarkup
from config import UZCARD_NUMBER, CARD_OWNER, MIN_PAYMENT
from database import cursor

def balans_menu():
    keyboard = [
        ["💳 Hisobni to‘ldirish"],
        ["⬅️ Orqaga"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def balans_handler(update, context):
    telegram_id = update.message.from_user.id
    cursor.execute('SELECT balans, sarflangan, vip FROM users WHERE telegram_id=?', (telegram_id,))
    user = cursor.fetchone()
    if user:
        balans, sarflangan, vip = user
    else:
        balans, sarflangan, vip = 0, 0, 0

    vip_status = "✅ Ha" if vip else "❌ Yo‘q"

    await update.message.reply_text(
        f"💳 Balansingiz: {balans} so‘m\n"
        f"💸 Sarflangan: {sarflangan} so‘m\n"
        f"👑 VIP: {vip_status}",
        reply_markup=balans_menu()
    )

async def hisob_toldirish(update, context):
    await update.message.reply_text(
        f"💳 Hisobni to‘ldirish uchun:\n\n"
        f"Karta raqam: {UZCARD_NUMBER}\n"
        f"Egasining ismi: {CARD_OWNER}\n"
        f"Minimal to‘lov: {MIN_PAYMENT} so‘m\n\n"
        "1️⃣ To‘lov qiling\n"
        "2️⃣ «✅ To‘lov qildim» tugmasini bosing\n"
        "3️⃣ Chek rasmini yuboring",
        reply_markup=back_button()
    )
