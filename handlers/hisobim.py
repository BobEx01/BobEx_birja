from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn
from handlers.start import asosiy_menu

BONUS_MIqdori = 50000

async def hisobim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Foydalanuvchini tekshirish
    cursor.execute("SELECT balans, bonus_berildi, paketlar, toldirilgan FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        balans, bonus_berildi, paketlar, toldirilgan = user_data

        # Bonus berilmagan bo‘lsa
        if not bonus_berildi:
            balans += BONUS_MIqdori
            cursor.execute(
                "UPDATE foydalanuvchilar SET balans = ?, bonus_berildi = 1 WHERE user_id = ?",
                (balans, user_id)
            )
            conn.commit()
    else:
        # Yangi foydalanuvchi - bonus bilan
        balans = BONUS_MIqdori
        paketlar = 'Yo‘q'
        toldirilgan = 0
        cursor.execute(
            "INSERT INTO foydalanuvchilar (user_id, balans, bonus_berildi, paketlar, toldirilgan) VALUES (?, ?, 1, ?, ?)",
            (user_id, balans, paketlar, toldirilgan)
        )
        conn.commit()

    # Ma'lumotlarni yana chaqirish
    cursor.execute("SELECT balans, paketlar, toldirilgan FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    balans, paketlar, toldirilgan = cursor.fetchone()

    text = (
        f"💳 *Hisobingiz haqida ma'lumot:*\n\n"
        f"🆔 Foydalanuvchi ID: `{user_id}`\n"
        f"💰 Balans: *{balans:,} so'm*\n"
        f"🎁 Olingan paketlar: {paketlar}\n"
        f"➕ To‘ldirilgan summa: {toldirilgan:,} so'm\n"
        f"🎉 Bonus: {BONUS_MIqdori:,} so'm (faqat bir marta beriladi)\n\n"
        "_Balans faqat xizmatlar uchun sarflanadi va qaytarilmaydi._"
    )

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=asosiy_menu())
