# handlers/shofyor_korish.py

from database import cursor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import RAQAM_NARX

async def shofyor_korish(update, context):
    cursor.execute('SELECT * FROM shofyor_elonlar ORDER BY premium DESC, sanasi DESC LIMIT 10')
    elonlar = cursor.fetchall()

    if not elonlar:
        await update.message.reply_text("Hozircha shofyor e’lonlari mavjud emas.")
        return

    for elon in elonlar:
        elon_id = elon[0]
        viloyat = elon[2]
        tuman = elon[3]
        mashina = elon[4]
        sigim = elon[5]
        narx = elon[6]

        text = (
            f"🏷 Shofyor E’lon ID: {elon_id}\n"
            f"📍 Manzil: {viloyat}, {tuman}\n"
            f"🚚 Mashina turi: {mashina}\n"
            f"⚖️ Sig‘im: {sigim}\n"
            f"💰 Narx: {narx} so‘m\n"
        )

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"📞 Raqam olish ({RAQAM_NARX} so‘m)", callback_data=f"shofyor_raqam_{elon_id}")
        ]])

        await update.message.reply_text(text, reply_markup=keyboard)
