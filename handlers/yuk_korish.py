from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database import cursor, conn
from config import RAQAM_NARX
from handlers.start import asosiy_menu
import asyncio

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


# Tumanlarni ko'rish callback
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


# E'lonlarni ko'rish callback
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

        # Ko‘rilganlar sonini yangilash
        cursor.execute("UPDATE yuk_elonlar SET korilgan = korilgan + 1 WHERE id = ?", (elon_id,))
        conn.commit()

        premium_text = ""
        if premium == 2:
            premium_text = "🌟 *SUPER E'lon*\n\n"
        elif premium == 1:
            premium_text = "💎 *VIP E'lon*\n\n"

        text = (
            f"{premium_text}"
            f"🏷 *Yuk E’lon ID:* {elon_id}\n"
            f"📍 *Manzil:* {viloyat}, {tuman}\n"
            f"🚩 *Qayerdan:* {qayerdan}\n"
            f"🏁 *Qayerga:* {qayerga}\n"
            f"⚖️ *Og‘irligi:* {ogirlik}\n"
            f"🚚 *Mashina turi:* {mashina}\n"
            f"💰 *Narx:* {narx} so‘m\n"
            f"👁 *Ko‘rilgan:* {korilgan + 1} marta\n"
        )

        # Raqam olish uchun tugma
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"📞 Raqam olish ({RAQAM_NARX} so‘m)", callback_data=f"yuk_raqam_{elon_id}")
        ]])

        await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

    # Pastda orqaga va asosiy menyu tugmalari
    await query.message.reply_text(
        "Tanlang:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tumanlar_{viloyat}")],
            [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")]
        ])
    )


# Orqaga viloyatlar tugmasiasync def orqaga_viloyatlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await yuk_korish(update.callback_query, context)


# Orqaga tumanlar tugmasi
async def orqaga_tumanlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    viloyat = query.data.split('_')[2]
    await tumanlar_korish(update, context)
