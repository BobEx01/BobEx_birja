from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn
from config import VIP_NARX, SUPER_NARX
from handlers.start import asosiy_menu

async def vip_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    natija = cursor.fetchone()
    
    if not natija or natija[0] < VIP_NARX:
        await query.edit_message_text("❌ Balansingiz yetarli emas. Avval balansni to‘ldiring.")
        return

    cursor.execute("UPDATE foydalanuvchilar SET balans = balans - ? WHERE user_id = ?", (VIP_NARX, user_id))
    cursor.execute("UPDATE yuk_elonlar SET premium = 2 WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    conn.commit()

    await query.edit_message_text("✅ E'loningiz VIP holatga muvaffaqiyatli o‘tkazildi!")

async def super_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    natija = cursor.fetchone()
    
    if not natija or natija[0] < SUPER_NARX:
        await query.edit_message_text("❌ Balansingiz yetarli emas. Avval balansni to‘ldiring.")
        return

    cursor.execute("UPDATE foydalanuvchilar SET balans = balans - ? WHERE user_id = ?", (SUPER_NARX, user_id))
    cursor.execute("UPDATE yuk_elonlar SET premium = 3 WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    conn.commit()

    await query.edit_message_text("✅ E'loningiz SUPER holatga muvaffaqiyatli o‘tkazildi!")
