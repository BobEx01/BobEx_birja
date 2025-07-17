from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import cursor, conn
from config import PREMIUM_ELON_NARX, ADMIN_ID


async def premium_elon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
        return

    balans = result[0]
    if balans < PREMIUM_ELON_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. Premium e’lon uchun {PREMIUM_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    # Balansdan pul yechish
    cursor.execute(
        'UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ? WHERE user_id = ?',
        (PREMIUM_ELON_NARX, PREMIUM_ELON_NARX, user_id)
    )
    conn.commit()

    await update.message.reply_text(
        "✅ Premium e’lon muvaffaqiyatli faollashtirildi!\n"
        "Endi e’loningiz ro‘yxatda yuqorida chiqadi."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📦 User {user_id} premium e’lon sotib oldi."
    )


async def premium_elon_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    if len(data) < 4:
        await query.edit_message_text("❌ Ma'lumot yetarli emas.")
        return

    _, _, elon_id, user_id = data
    user_id = int(user_id)

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

    # E'lonni premium qilish
    cursor.execute(
        'UPDATE yuk_elonlar SET premium = 1 WHERE id = ?',
        (elon_id,)
    )

    conn.commit()

    await query.edit_message_text("✅ E’lon Premium qilindi! Endi u ro‘yxatda yuqorida ko‘rsatiladi.")

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📦 User {user_id} premium e’lon CALLBACK orqali sotib oldi."
    )
