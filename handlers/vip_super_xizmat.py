from telegram import Update
from telegram.ext import ContextTypes
from database import balans_olish, balans_oshirish, cursor, conn
from config import VIP_ELON_NARX, SUPER_ELON_NARX, ADMIN_ID


async def vip_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balans = balans_olish(user_id)

    if balans < VIP_ELON_NARX:
        await update.message.reply_text(f"❌ Balansingiz yetarli emas. VIP e’lon uchun {VIP_ELON_NARX} so‘m kerak.")
        return

    cursor.execute("""
        UPDATE foydalanuvchilar
        SET balans = balans - ?, sarflangan = sarflangan + ?
        WHERE user_id = ?
    """, (VIP_ELON_NARX, VIP_ELON_NARX, user_id))
    conn.commit()

    cursor.execute("""
        UPDATE shofyor_elonlar
        SET premium = 2
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    """, (user_id,))
    conn.commit()

    balans_oshirish(user_id, 0)  # balans yangilanishi uchun chaqirildi

    await update.message.reply_text("✅ E’loningiz VIP holatga o‘tkazildi! 1 ta telefon raqamni bepul olishingiz mumkin.")
    await context.bot.send_message(ADMIN_ID, f"📢 Foydalanuvchi {user_id} VIP e’lon sotib oldi.")


async def super_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balans = balans_olish(user_id)

    if balans < SUPER_ELON_NARX:
        await update.message.reply_text(f"❌ Balansingiz yetarli emas. Super e’lon uchun {SUPER_ELON_NARX} so‘m kerak.")
        return

    cursor.execute("""
        UPDATE foydalanuvchilar
        SET balans = balans - ?, sarflangan = sarflangan + ?
        WHERE user_id = ?
    """, (SUPER_ELON_NARX, SUPER_ELON_NARX, user_id))
    conn.commit()

    cursor.execute("""
        UPDATE shofyor_elonlar
        SET premium = 3
        WHERE user_id = ? ORDER BY sanasi DESC LIMIT 1
    """, (user_id,))
    conn.commit()

    balans_oshirish(user_id, 0)  # balans yangilanishi uchun chaqirildi

    await update.message.reply_text("✅ E’loningiz Super holatga o‘tkazildi! 3 ta telefon raqamni bepul olishingiz mumkin.")
    await context.bot.send_message(ADMIN_ID, f"📢 Foydalanuvchi {user_id} Super e’lon sotib oldi.")
