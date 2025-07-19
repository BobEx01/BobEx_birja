from database import cursor, conn
from config import VIP_ELON_NARX, SUPER_ELON_NARX, ADMIN_ID
from handlers.start import asosiy_menu
import datetime


async def vip_elon_qilish(update, context):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
        return

    balans = result[0]
    if balans < VIP_ELON_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. VIP e’lon uchun {VIP_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    cursor.execute(
        'UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ? WHERE user_id = ?',
        (VIP_ELON_NARX, VIP_ELON_NARX, user_id)
    )
    conn.commit()

    await update.message.reply_text(
        "✅ VIP e’lon muvaffaqiyatli faollashtirildi!\n"
        "Endi e’loningiz ro‘yxatda yuqoriroqda chiqadi.\n"
        "Bonus: 1 ta telefon raqamni bepul olasiz!"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📦 User {user_id} VIP e’lon sotib oldi."
    )


async def super_elon_qilish(update, context):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
        return

    balans = result[0]
    if balans < SUPER_ELON_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. Super e’lon uchun {SUPER_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    cursor.execute(
        'UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ? WHERE user_id = ?',
        (SUPER_ELON_NARX, SUPER_ELON_NARX, user_id)
    )
    conn.commit()

    await update.message.reply_text(
        "✅ Super e’lon muvaffaqiyatli faollashtirildi!\n"
        "Endi e’loningiz maxsus tavsiya blokida va har doim yuqorida chiqadi.\n"
        "Bonus: 3 ta telefon raqamni bepul olasiz!"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📦 User {user_id} Super e’lon sotib oldi."
    )
