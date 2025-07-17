from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from database import cursor
from config import RAQAM_NARX
from handlers.start import asosiy_menu


async def yuk_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT viloyat, COUNT(*) FROM yuk_elonlar GROUP BY viloyat")
    viloyatlar = cursor.fetchall()

    if not viloyatlar:
        await update.message.reply_text("Hozircha yuk e’lonlari mavjud emas.")
        return

    keyboard = []
    for viloyat, count in viloyatlar:
        keyboard.append([
            InlineKeyboardButton(f"{viloyat} ({count} ta)", callback_data=f"viloyat_{viloyat}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")
    ])

    await update.message.reply_text("Viloyatni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))


async def tumanlar_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    viloyat = query.data.split('_')[1]

    cursor.execute("SELECT tuman, COUNT(*) FROM yuk_elonlar WHERE viloyat = ? GROUP BY tuman", (viloyat,))
    tumanlar = cursor.fetchall()

    if not tumanlar:
        await query.edit_message_text("Bu viloyatda hozircha e’lon mavjud emas.", reply_markup=asosiy_menu())
        return

    keyboard = []
    for tuman, count in tumanlar:
        keyboard.append([
            InlineKeyboardButton(f"{tuman} ({count} ta)", callback_data=f"tuman_{viloyat}_{tuman}")
        ])
    
    keyboard.append([
        InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_viloyatlar"),
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")
    ])

    await query.edit_message_text(f"{viloyat} viloyati uchun tumanlardan birini tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))


async def elonlar_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, viloyat, tuman = query.data.split('_')

    cursor.execute(
        "SELECT id, qayerdan, qayerga, ogirlik, mashina, narx FROM yuk_elonlar WHERE viloyat = ? AND tuman = ? ORDER BY premium DESC, sanasi DESC",
        (viloyat, tuman)
    )
    elonlar = cursor.fetchall()

    if not elonlar:
        await query.edit_message_text("Bu tumanda yuk e’lonlari topilmadi.", reply_markup=asosiy_menu())
        return

    for elon in elonlar:
        elon_id, qayerdan, qayerga, ogirlik, mashina, narx = elon

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

        await query.message.reply_text(text, reply_markup=keyboard)

    await query.message.reply_text(
        "Tanlang:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tumanlar_{viloyat}")],
            [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")]
        ])
    )


async def orqaga_viloyatlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await yuk_korish(query, context)


async def orqaga_tumanlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    viloyat = query.data.split('_')[2]
    await tumanlar_korish(update, context)


async def asosiy_menyu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🏠 Bosh menyu:", reply_markup=asosiy_menu())
    return ConversationHandler.END
