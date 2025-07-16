# handlers/yuk_korish.py

from database import cursor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import RAQAM_NARX

async def yuk_korish(update, context):
    cursor.execute('SELECT * FROM yuk_elonlar ORDER BY premium DESC, sanasi DESC LIMIT 10')
    elonlar = cursor.fetchall()

    if not elonlar:
        await update.message.reply_text("Hozircha yuk e’lonlari mavjud emas.")
        return

    for elon in elonlar:
        elon_id = elon[0]
        viloyat = elon[2]
        tuman = elon[3]
        qayerdan = elon[4]
        qayerga = elon[5]
        ogirlik = elon[6]
        mashina = elon[7]
        narx = elon[8]

        text = (
            f"🏷 Yuk E’lon ID: {elon_id}\n"
            f"📍 Manzil: {viloyat}, {tuman}\n"
            f"🚩 Qayerdan: {qayerdan}\n"
            f"🏁 Qayerga: {qayerga}\n"
            f"⚖️ Og‘irligi: {ogirlik}\n"
            f"🚚 Mashina turi: {mashina}\n"
            f"💰 Narx: {narx} so‘m\n"
        )

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"📞 Raqam olish ({RAQAM_NARX} so‘m)", callback_data=f"yuk_raqam_{elon_id}")
        ]])

        await update.message.reply_text(text, reply_markup=keyboard)
