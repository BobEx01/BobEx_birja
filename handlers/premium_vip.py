from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import cursor, conn, balans_olish, balans_oshirish
from config import VIP_ELON_NARX, SUPER_ELON_NARX, ADMIN_ID


async def vip_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balans = balans_olish(user_id)

    if balans < VIP_ELON_NARX:
        await update.message.reply_text("❌ VIP e’lon uchun balansingiz yetarli emas.")
        return

    cursor.execute('''
        UPDATE foydalanuvchilar
        SET balans = balans - ?, sarflangan = sarflangan + ?
        WHERE user_id = ?
    ''', (VIP_ELON_NARX, VIP_ELON_NARX, user_id))

    cursor.execute('''
        UPDATE yuk_elonlar
        SET premium = 2
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    ''', (user_id,))

    conn.commit()

    await update.message.reply_text("✅ E’loningiz VIP holatga muvaffaqiyatli o‘tkazildi!")
    await context.bot.send_message(ADMIN_ID, f"📢 <b>{user_id}</b> VIP e’lon xarid qildi.", parse_mode='HTML')


async def super_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balans = balans_olish(user_id)

    if balans < SUPER_ELON_NARX:
        await update.message.reply_text("❌ Super e’lon uchun balansingiz yetarli emas.")
        return

    cursor.execute('''
        UPDATE foydalanuvchilar
        SET balans = balans - ?, sarflangan = sarflangan + ?
        WHERE user_id = ?
    ''', (SUPER_ELON_NARX, SUPER_ELON_NARX, user_id))

    cursor.execute('''
        UPDATE yuk_elonlar
        SET premium = 3
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    ''', (user_id,))

    conn.commit()

    await update.message.reply_text("✅ E’loningiz Super holatga muvaffaqiyatli o‘tkazildi!")
    await context.bot.send_message(ADMIN_ID, f"📢 <b>{user_id}</b> Super e’lon xarid qildi.", parse_mode='HTML')
