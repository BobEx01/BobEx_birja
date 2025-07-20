from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database import cursor, conn
from config import RAQAM_NARX
from handlers.start import asosiy_menu

# Viloyatlar bo'yicha yuk e'lonlarini ko'rish
async def yuk_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT viloyat, COUNT(*) FROM yuk_elonlar GROUP BY viloyat")
    viloyatlar = cursor.fetchall()

    if not viloyatlar:
        await update.message.reply_text("Hozircha yuk e’lonlari mavjud emas.")
        return

    keyboard = [
        [InlineKeyboardButton(f"{viloyat} ({count} ta)", callback_data=f"viloyat_{viloyat}")]
        for viloyat, count in viloyatlar
    ]

    keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")])

    await update.message.reply_text("Viloyatni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))


# Tumanlar bo'yicha yuk e'lonlarini ko'rish
async def tumanlar_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    viloyat = query.data.split('_')[1]

    cursor.execute("SELECT tuman, COUNT(*) FROM yuk_elonlar WHERE viloyat = ? GROUP BY tuman", (viloyat,))
    tumanlar = cursor.fetchall()

    if not tumanlar:
        await query.edit_message_text("Bu viloyatda hozircha e’lon mavjud emas.", reply_markup=asosiy_menu())
        return

    keyboard = [
        [InlineKeyboardButton(f"{tuman} ({count} ta)", callback_data=f"tuman_{viloyat}_{tuman}")]
        for tuman, count in tumanlar
    ]
    keyboard.append([
        InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_viloyatlar"),
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")
    ])

    await query.edit_message_text(f"{viloyat} viloyati uchun tumanlardan birini tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))


# E'lonlarni ko‘rsatish
async def elonlar_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, viloyat, tuman = query.data.split('_')

    cursor.execute(
        "SELECT id, qayerdan, qayerga, ogirlik, mashina, narx, premium, korilgan FROM yuk_elonlar WHERE viloyat = ? AND tuman = ? ORDER BY premium DESC, sanasi DESC",
        (viloyat, tuman)
    )
    elonlar = cursor.fetchall()

    if not elonlar:
        await query.edit_message_text("Bu tumanda yuk e’lonlari topilmadi.", reply_markup=asosiy_menu())
        return

    for elon in elonlar:
        elon_id, qayerdan, qayerga, ogirlik, mashina, narx, premium, korilgan = elon

        cursor.execute("UPDATE yuk_elonlar SET korilgan = korilgan + 1 WHERE id = ?", (elon_id,))
        conn.commit()

        text = ""
        if premium == 2:
            text += "🌟 SUPER E’LON 🌟\n\n"
        elif premium == 1:
            text += "💎 VIP E’LON 💎\n\n"

        text += (
            f"🏷 E’lon ID: {elon_id}\n"
            f"📍 Manzil: {viloyat}, {tuman}\n"
            f"🚩 Qayerdan: {qayerdan}\n"
            f"🏁 Qayerga: {qayerga}\n"
            f"⚖️ Og‘irligi: {ogirlik}\n"
            f"🚚 Mashina: {mashina}\n"
            f"💰 Narx: {narx} so‘m\n"
            f"👁 Ko‘rilgan: {korilgan + 1} marta"
        )

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"📞 Raqam olish ({RAQAM_NARX} so‘m)", callback_data=f"yuk_raqam_{elon_id}")
        ]])

        await query.message.reply_text(text, reply_markup=keyboard)

    await query.message.reply_text(
        "Tanlang:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tumanlar_{viloyat}")],
            [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")]
        ])
    )


# Orqaga viloyatlar
async def orqaga_viloyatlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await yuk_korish(update, context)


# Orqaga tumanlar
async def orqaga_tumanlar(update: Update, context: ContextTypes.
                          DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split('_')
    viloyat = data[2]
    context.user_data['viloyat'] = viloyat
    await tumanlar_korish(update, context)
