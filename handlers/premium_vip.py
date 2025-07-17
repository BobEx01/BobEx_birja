from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn
from config import VIP_NARX, ADMIN_ID
from handlers.start import asosiy_menu
import datetime


async def vip_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
        return

    balans = result[0]
    if balans < VIP_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. VIP olish uchun {VIP_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    vip_muddati = datetime.datetime.now() + datetime.timedelta(days=30)
    cursor.execute("""
        UPDATE foydalanuvchilar 
        SET balans = balans - ?, sarflangan = sarflangan + ?, vip = 1, vip_muddati = ?
        WHERE user_id = ?
    """, (VIP_NARX, VIP_NARX, vip_muddati.strftime('%Y-%m-%d'), user_id))
    conn.commit()

    await update.message.reply_text(
        "👑 VIP statusingiz 30 kun davomida faollashtirildi!\n\n"
        "VIP bo‘lsangiz barcha funksiyalar bepul bo‘ladi.",
        reply_markup=asosiy_menu()
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👑 User {user_id} VIP paket sotib oldi. Muddati: {vip_muddati.strftime('%Y-%m-%d')}."
    )
