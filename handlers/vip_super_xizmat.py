from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn, balans_olish, balans_oshirish
from config import VIP_NARX, SUPER_NARX, ADMIN_ID


async def vip_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balans = balans_olish(user_id)

    if balans < VIP_NARX:
        await update.message.reply_text(f"❌ VIP e'lon uchun balansingiz yetarli emas. Kerakli miqdor: {VIP_NARX} so'm")
        return

    cursor.execute('''
        UPDATE shofyor_elonlar
        SET premium = 2
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    ''', (user_id,))
    conn.commit()

    cursor.execute('UPDATE foydalanuvchilar SET balans = balans - ? WHERE user_id = ?', (VIP_NARX, user_id))
    balans_oshirish(user_id, 1)  # Bonus uchun 1 ta raqam olish
    conn.commit()

    await update.message.reply_text("✅ E’loningiz VIP holatga o‘tkazildi! 1 ta telefon raqam olish bonusingiz ham qo‘shildi.")
    await context.bot.send_message(ADMIN_ID, f"👑 User {user_id} VIP e’lon sotib oldi.")


async def super_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balans = balans_olish(user_id)

    if balans < SUPER_NARX:
        await update.message.reply_text(f"❌ Super e'lon uchun balansingiz yetarli emas. Kerakli miqdor: {SUPER_NARX} so'm")
        return

    cursor.execute('''
        UPDATE shofyor_elonlar
        SET premium = 3
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    ''', (user_id,))
    conn.commit()

    cursor.execute('UPDATE foydalanuvchilar SET balans = balans - ? WHERE user_id = ?', (SUPER_NARX, user_id))
    balans_oshirish(user_id, 3)  # Bonus uchun 3 ta raqam olish
    conn.commit()

    await update.message.reply_text("✅ E’loningiz SUPER holatga o‘tkazildi! 3 ta telefon raqam olish bonusingiz ham qo‘shildi.")
    await context.bot.send_message(ADMIN_ID, f"🌟 User {user_id} SUPER e’lon sotib oldi.")
