from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn
from handlers.start import asosiy_menu

BONUS_MIqdori = 50000  # 50 ming so'm bonus

async def hisobim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Foydalanuvchini tekshiramiz
    cursor.execute("SELECT balans, bonus_berildi, paketlar, toldirilgan FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        balans, bonus_berildi, paketlar, toldirilgan = user_data

        # Bonus hali berilmagan bo‘lsa
        if not bonus_berildi:
            balans += BONUS_MIqdori
            cursor.execute("UPDATE foydalanuvchilar SET balans = ?, bonus_berildi = 1 WHERE user_id = ?", (balans, user_id))
            conn.commit()

    else:
        # Yangi foydalanuvchi - bonus beriladi
        balans = BONUS_MIqdori
        paketlar = "Yo‘q"
        toldirilgan = 0
        cursor.execute("INSERT INTO foydalanuvchilar (user_id, balans, bonus_berildi, paketlar, toldirilgan) VALUES (?, ?, 1, ?, ?)",
                       (user_id, balans, paketlar, toldirilgan))
        conn.commit()

    # Yangilangan ma'lumotlarni olish
    cursor.execute("SELECT balans, paketlar, toldirilgan FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    balans, paketlar, toldirilgan = cursor.fetchone()

    text = (
        f"💳 *Hisobingiz haqida ma'lumot:*\n\n"
        f"🆔 ID raqamingiz: `{user_id}`\n"
        f"💰 Balans: *{balans:,} so'm*\n"
        f"🎁 Olingan paketlar: {paketlar}\n"
        f"➕ Umumiy to‘ldirilgan: *{toldirilgan:,} so'm*\n"
        f"🎉 Bir martalik bonus: *{BONUS_MIqdori:,} so'm*\n\n"
        "_Balansingiz faqat xizmatlar uchun ishlatiladi va qaytarilmaydi._"
    )

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=asosiy_menu())
