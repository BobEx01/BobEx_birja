# vip_super_xizmat.py

from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn, balans_olish
from config import VIP_NARX, SUPER_NARX
from handlers.start import asosiy_menu

async def vip_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    balans = balans_olish(user_id)

    if balans < VIP_NARX:
        await query.edit_message_text("❌ Balansingiz yetarli emas. VIP uchun balans to‘ldiring.")
        return

    cursor.execute("UPDATE foydalanuvchilar SET balans = balans - ? WHERE user_id = ?", (VIP_NARX, user_id))
    conn.commit()

    await query.edit_message_text("✅ VIP e’lon holati faollashtirildi!")
    await context.bot.send_message(user_id, "🏠 Bosh menyuga qaytdingiz:", reply_markup=asosiy_menu())

async def super_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    balans = balans_olish(user_id)

    if balans < SUPER_NARX:
        await query.edit_message_text("❌ Balansingiz yetarli emas. Super uchun balans to‘ldiring.")
        return

    cursor.execute("UPDATE foydalanuvchilar SET balans = balans - ? WHERE user_id = ?", (SUPER_NARX, user_id))
    conn.commit()

    await query.edit_message_text("✅ Super e’lon holati faollashtirildi!")
    await context.bot.send_message(user_id, "🏠 Bosh menyuga qaytdingiz:", reply_markup=asosiy_menu())
