from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import cursor, conn
from config import VIP_ELON_NARX, SUPER_ELON_NARX
from handlers.start import asosiy_menu

# VIP E'lon faollashtirish
async def vip_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')  # Format: vip_elon_userid|sanasi
    if len(data) >= 3:
        user_id_sanasi = data[2]
        user_id, sanasi = user_id_sanasi.split('|')
        
        cursor.execute(
            "UPDATE yuk_elonlar SET premium = 1 WHERE user_id = ? AND sanasi = ?",
            (user_id, sanasi)
        )
        conn.commit()

        await query.edit_message_text(
            "✅ *VIP E'lon faollashtirildi!*\n"
            "📌 E'loningiz ustun joyda ko‘rsatiladi.\n"
            "📆 Amal qilish muddati: 24 soat.\n"
            "💎 VIP belgisi ko‘rinadi.\n\n"
            "🏠 Bosh menyuga qayting:",
            reply_markup=asosiy_menu(),
            parse_mode='Markdown'
        )

# Super E'lon faollashtirish
async def super_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')  # Format: super_elon_userid|sanasi
    if len(data) >= 3:
        user_id_sanasi = data[2]
        user_id, sanasi = user_id_sanasi.split('|')
        
        cursor.execute(
            "UPDATE yuk_elonlar SET premium = 2 WHERE user_id = ? AND sanasi = ?",
            (user_id, sanasi)
        )
        conn.commit()

        await query.edit_message_text(
            "✅ *SUPER E'lon faollashtirildi!*\n"
            "🚀 E'loningiz barcha elonlardan yuqorida ko‘rsatiladi.\n"
            "📆 Amal qilish muddati: 24 soat.\n"
            "🌟 Super belgi ko‘rinadi.\n\n"
            "🏠 Bosh menyuga qayting:",
            reply_markup=asosiy_menu(),
            parse_mode='Markdown'
        )
