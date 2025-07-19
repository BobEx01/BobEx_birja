from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn, balans_olish, balans_oshirish
from config import VIP_ELON_NARX, SUPER_ELON_NARX, ADMIN_ID


async def vip_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balans = balans_olish(user_id)

    if balans < VIP_ELON_NARX:
        await update.message.reply_text("❌ VIP e’lon uchun balansingiz yetarli emas. Iltimos, avval balansingizni to‘ldiring.")
        return

    cursor.execute('''
        UPDATE shofyor_elonlar
        SET premium = 2
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    ''', (user_id,))
    cursor.execute('''
        UPDATE foydalanuvchilar
        SET balans = balans - ?, sarflangan = sarflangan + ?, paket_soni = paket_soni + 1
        WHERE user_id = ?
    ''', (VIP_ELON_NARX, VIP_ELON_NARX, user_id))
    balans_oshirish(user_id, 1)  # 1 ta raqam olish bonusi qo‘shiladi
    conn.commit()

    await update.message.reply_text("✅ E’loningiz VIP holatiga o‘tkazildi. 1 ta telefon raqamni bepul olishingiz mumkin.")
    await context.bot.send_message(ADMIN_ID, f"👤 {user_id} foydalanuvchi VIP e’lon aktiv qildi.")


async def super_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balans = balans_olish(user_id)

    if balans < SUPER_ELON_NARX:
        await update.message.reply_text("❌ Super e’lon uchun balansingiz yetarli emas. Iltimos, avval balansingizni to‘ldiring.")
        return

    cursor.execute('''
        UPDATE shofyor_elonlar
        SET premium = 3
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    ''', (user_id,))
    cursor.execute('''
        UPDATE foydalanuvchilar
        SET balans = balans - ?, sarflangan = sarflangan + ?, paket_soni = paket_soni + 3
        WHERE user_id = ?
    ''', (SUPER_ELON_NARX, SUPER_ELON_NARX, user_id))
    balans_oshirish(user_id, 3)  # 3 ta raqam olish bonusi qo‘shiladi
    conn.commit()

    await update.message.reply_text("✅ E’loningiz SUPER holatga o‘tkazildi. 3 ta telefon raqamni bepul olishingiz mumkin.")
    await context.bot.send_message(ADMIN_ID, f"👤 {user_id} foydalanuvchi SUPER e’lon aktiv qildi.")
