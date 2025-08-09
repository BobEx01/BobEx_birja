from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database import cursor
from keyboards.menu import main_menu as asosiy_menu

async def elonlarim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    print(f"🟩 Elonlarim handler chaqirildi, user_id: {user_id}")

    javob = ""

    # Yuk e'lonlar
    cursor.execute("""
        SELECT id, qayerdan, qayerga, ogirlik, mashina, narx, premium, sanasi, muddat, korilgan, raqam_olingan
        FROM yuk_elonlar WHERE user_id = ?
    """, (user_id,))
    yuk_elonlar = cursor.fetchall()

    if yuk_elonlar:
        javob += "🚚 <b>Yuk E'lonlaringiz:</b>\n"
        for elon in yuk_elonlar:
            elon_id, qayerdan, qayerga, ogirlik, mashina, narx, premium, sanasi, muddat, korilgan, raqam_olingan = elon
            javob += (
                f"🆔 ID: {elon_id}\n"
                f"📍 Qayerdan: {qayerdan} ➡️ {qayerga}\n"
                f"⚖️ Og‘irligi: {ogirlik}\n"
                f"🚚 Mashina: {mashina}\n"
                f"💰 Narx: {narx} so‘m\n"
                f"💎 Premium: {'✅' if premium else '❌'}\n"
                f"🗓 Sana: {sanasi}\n"
                f"📆 Muddat: {muddat or 'Ko‘rsatilmagan'}\n"
                f"👁 Ko‘rilgan: {korilgan} marta\n"
                f"📞 Raqam olingan: {raqam_olingan} marta\n\n"
            )

    # Shofyor e'lonlar
    cursor.execute("""
        SELECT id, qayerdan, qayerga, ism, telefon, narx, premium, sanasi, muddat, korilgan, raqam_olingan
        FROM shofyor_elonlar WHERE user_id = ?
    """, (user_id,))
    shofyor_elonlar = cursor.fetchall()

    if shofyor_elonlar:
        javob += "🧑‍✈️ <b>Shofyor E'lonlaringiz:</b>\n"
        for elon in shofyor_elonlar:
            elon_id, qayerdan, qayerga, ism, telefon, narx, premium, sanasi, muddat, korilgan, raqam_olingan = elon
            javob += (
                f"🆔 ID: {elon_id}\n"
                f"📍 Qayerdan: {qayerdan} ➡️ {qayerga}\n"
                f"🧑‍✈️ Ism: {ism}\n"
                f"📞 Tel: {telefon}\n"
                f"💰 Narx: {narx} so‘m\n"
                f"💎 Premium: {'✅' if premium else '❌'}\n"
                f"🗓 Sana: {sanasi}\n"
                f"📆 Muddat: {muddat or 'Ko‘rsatilmagan'}\n"
                f"👁 Ko‘rilgan: {korilgan} marta\n"
                f"📞 Raqam olingan: {raqam_olingan} marta\n\n"
            )

    if not javob:
        javob = "❗️Sizda hali hech qanday e’lon mavjud emas."

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Orqaga", callback_data='asosiy_menu')]
    ])

    await update.message.reply_text(javob, reply_markup=keyboard, parse_mode='HTML')
