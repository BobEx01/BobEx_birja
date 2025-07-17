from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database import cursor, conn
from config import PREMIUM_ELON_NARX, ADMIN_ID


# E'LONLARNI CHIQARISH FUNKSIYASI
async def elonlar_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, viloyat, tuman = query.data.split('_')

    cursor.execute(
        "SELECT id, qayerdan, qayerga, ogirlik, mashina, narx, premium FROM yuk_elonlar WHERE viloyat = ? AND tuman = ? ORDER BY premium DESC, sanasi DESC",
        (viloyat, tuman)
    )
    elonlar = cursor.fetchall()

    if not elonlar:
        await query.edit_message_text("Bu tumanda yuk e’lonlari topilmadi.")
        return

    for elon in elonlar:
        elon_id, qayerdan, qayerga, ogirlik, mashina, narx, premium = elon

        text = (
            f"🏷 Yuk E’lon ID: {elon_id}\n"
            f"📍 Manzil: {viloyat}, {tuman}\n"
            f"🚩 Qayerdan: {qayerdan}\n"
            f"🏁 Qayerga: {qayerga}\n"
            f"⚖️ Og‘irligi: {ogirlik}\n"
            f"🚚 Mashina turi: {mashina}\n"
            f"💰 Narx: {narx} so‘m\n"
        )

        if premium == 1:
            text = "💎 PREMIUM E'LON 💎\n\n" + text

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Premium qilish", callback_data=f"premium_elon_{elon_id}")],
        ])

        await query.message.reply_text(text, reply_markup=keyboard)


# PREMIUMGA AYLANTRISH CALLBACK FUNKSIYASI
async def premium_elon_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    if len(data) < 3:
        await query.edit_message_text("❌ Ma'lumot noto‘g‘ri keldi.")
        return

    _, _, elon_id = data
    elon_id = int(elon_id)
    user_id = query.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await query.edit_message_text("❌ Foydalanuvchi topilmadi.")
        return

    balans = result[0]
    if balans < PREMIUM_ELON_NARX:
        await query.edit_message_text(
            f"❌ Balansingiz yetarli emas. Premium e’lon uchun {PREMIUM_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    # Balansdan pul yechish
    cursor.execute(
        'UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ? WHERE user_id = ?',
        (PREMIUM_ELON_NARX, PREMIUM_ELON_NARX, user_id)
    )

    # E'lonni Premium qilish
    cursor.execute(
        'UPDATE yuk_elonlar SET premium = 1 WHERE id = ?',
        (elon_id,)
    )

    conn.commit()

    await query.edit_message_text("✅ E’lon Premium qilindi! Endi u ro‘yxatda yuqorida ko‘rsatiladi.")

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📦 User {user_id} premium e’lonni ID {elon_id} uchun sotib oldi."
    )
