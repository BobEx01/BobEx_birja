# handlers/shofyor_korish.py

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

    keyboard = []
    for viloyat, count in viloyatlar:
        keyboard.append([
            InlineKeyboardButton(f"{viloyat} ({count} ta)", callback_data=f"shof_vil_{viloyat}")
        ])

    keyboard.append([
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")
    ])

    await update.message.reply_text(
        "Viloyatni tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def shofyor_tumanlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    viloyat = query.data.split('_')[2]
    cursor.execute("SELECT tuman, COUNT(*) FROM shofyor_elonlar WHERE viloyat = ? GROUP BY tuman", (viloyat,))
    tumanlar = cursor.fetchall()

    if not tumanlar:
        await query.message.reply_text("Bu viloyatda shofyor e’lonlari yo‘q.")
        return

    keyboard = []
    for tuman, count in tumanlar:
        keyboard.append([
            InlineKeyboardButton(f"{tuman} ({count} ta)", callback_data=f"shof_tum_{viloyat}_{tuman}")
        ])

    keyboard.append([
        InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_viloyatlar_shofyor"),
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")
    ])

    await query.message.reply_text(
        f"{viloyat} viloyati uchun tumanlardan birini tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def shofyor_elonlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, _, viloyat, tuman = query.data.split('_')

    cursor.execute(
        "SELECT id, mashina, sigim, narx FROM shofyor_elonlar WHERE viloyat = ? AND tuman = ? ORDER BY premium DESC, sanasi DESC",
        (viloyat, tuman)
    )
    elonlar = cursor.fetchall()

    if not elonlar:
        await query.message.reply_text("Bu tumanda shofyor e’lonlari mavjud emas.")
        return

    for elon in elonlar:
        elon_id, mashina, sigim, narx = elon

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

        await query.message.reply_text(text, reply_markup=keyboard)

    # Navigatsion tugmalar
    keyboard_nav = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tumanlar_shofyor_{viloyat}")],
        [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")]
    ])

    await query.message.reply_text("Tanlang:", reply_markup=keyboard_nav)


# --- ORQAGA VILOYATLARGA ---
async def orqaga_viloyatlar_shofyor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await shofyor_korish(update, context)


# --- ORQAGA TUMANLARGA ---
async def orqaga_tumanlar_shofyor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    viloyat = query.data.split('_')[-1]
    await shofyor_tumanlar(query, context)


# --- ASOSIY MENYU HANDLER ---
async def asosiy_menyu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🏠 Bosh menyu:", reply_markup=asosiy_menu())
