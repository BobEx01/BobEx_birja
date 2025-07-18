from database import cursor
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config import RAQAM_NARX
from handlers.start import asosiy_menu


async def shofyor_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT viloyat, COUNT(*) FROM shofyor_elonlar GROUP BY viloyat")
    viloyatlar = cursor.fetchall()

    if not viloyatlar:
        await update.message.reply_text("Hozircha shofyor e’lonlari mavjud emas.")
        return

    keyboard = [
        [InlineKeyboardButton(f"{viloyat} ({count} ta)", callback_data=f"shof_vil_{viloyat}")]
        for viloyat, count in viloyatlar
    ]
    keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")])

    await update.message.reply_text("Viloyatni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))


async def shofyor_tumanlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    viloyat = query.data.split('_', 2)[2]
    cursor.execute("SELECT tuman, COUNT(*) FROM shofyor_elonlar WHERE viloyat = ? GROUP BY tuman", (viloyat,))
    tumanlar = cursor.fetchall()

    if not tumanlar:
        await query.message.reply_text("Bu viloyatda shofyor e’lonlari yo‘q.")
        return

    keyboard = [
        [InlineKeyboardButton(f"{tuman} ({count} ta)", callback_data=f"shof_tum_{viloyat}_{tuman}")]
        for tuman, count in tumanlar
    ]
    keyboard.append([
        InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_viloyatlar_shofyor"),
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")
    ])

    await query.message.reply_text(f"{viloyat} viloyati uchun tumanlardan birini tanlang:",
                                   reply_markup=InlineKeyboardMarkup(keyboard))


async def shofyor_elonlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, _, viloyat, tuman = query.data.split('_', 3)

    cursor.execute(
        "SELECT id, mashina, sigim, narx, korilgan FROM shofyor_elonlar WHERE viloyat = ? AND tuman = ? ORDER BY premium DESC, sanasi DESC",
        (viloyat, tuman)
    )
    elonlar = cursor.fetchall()

    if not elonlar:
        await query.message.reply_text("Bu tumanda shofyor e’lonlari mavjud emas.")
        return

    for elon in elonlar:
        elon_id, mashina, sigim, narx, korilgan = elon

        cursor.execute("UPDATE shofyor_elonlar SET korilgan = korilgan + 1 WHERE id = ?", (elon_id,))
        # connection.commit() ni olib tashladik
        cursor.connection.commit()

        text = (
            f"🏷 E’lon ID: {elon_id}\n"
            f"📍 Manzil: {viloyat}, {tuman}\n"
            f"🚚 Mashina: {mashina}\n"
            f"⚖️ Sig‘im: {sigim}\n"
            f"💰 Narx: {narx} so‘m\n"
            f"👁 Ko‘rilgan: {korilgan + 1} marta\n"
        )

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"📞 Raqam olish ({RAQAM_NARX} so‘m)", callback_data=f"shofyor_raqam_{elon_id}")
        ]])

        await query.message.reply_text(text, reply_markup=keyboard)

    nav_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tumanlar_shofyor_{viloyat}")],
        [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")]
    ])

    await query.message.reply_text("Tanlang:", reply_markup=nav_keyboard)


async def orqaga_viloyatlar_shofyor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await shofyor_korish(update, context)


async def orqaga_tumanlar_shofyor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split('_')
    viloyat = parts[-1]
    await shofyor_tumanlar(update, context)


async def asosiy_menyu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Xabar yuboring:")
