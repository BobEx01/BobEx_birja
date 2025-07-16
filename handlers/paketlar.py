# handlers/paketlar.py

from database import cursor, conn
from config import PAKET_10_NARX
import datetime

async def paketlar_handler(update, context):
    text = (
        "🎟 <b>Paketlar va Aksiyalar:</b>\n\n"
        "1️⃣ 10 ta raqam olish paketi - 186,000 so‘m (33% chegirma)\n"
        "2️⃣ Har juma kuni - <b>50% chegirma</b> barcha funksiyalar uchun!\n"
        "3️⃣ VIP tarif - 1,000,000 so‘m (30 kun davomida barcha xizmatlar bepul)\n\n"
        "Paket sotib olish uchun /paket_ol buyruqni yuboring."
    )
    await update.message.reply_text(text, parse_mode='HTML')

async def paket_ol(update, context):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM users WHERE telegram_id=?', (user_id,))
    result = cursor.fetchone()

    if not result or result[0] < PAKET_10_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. 10 ta paket uchun {PAKET_10_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    # Balansdan yechish va paketni berish
    cursor.execute('UPDATE users SET balans = balans - ?, sarflangan = sarflangan + ?, paket_soni = paket_soni + 10 WHERE telegram_id=?',
                   (PAKET_10_NARX, PAKET_10_NARX, user_id))
    conn.commit()

    await update.message.reply_text(
        "✅ 10 ta raqam olish paketi muvaffaqiyatli sotib olindi!\n"
        "Endi balansdan yechmasdan 10 ta raqam olishingiz mumkin."
    )
