from database import cursor, conn
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config import RAQAM_NARX, VIP_ELON_NARX, SUPER_ELON_NARX
from handlers.start import asosiy_menu
import datetime
import asyncio


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
        await query.message.reply_text("Bu viloyatda shofyor e’lonlari yo‘q.", reply_markup=asosiy_menu())
        return

    keyboard = [
        [InlineKeyboardButton(f"{tuman} ({count} ta)", callback_data=f"shof_tum_{viloyat}_{tuman}")]
        for tuman, count in tumanlar
    ]
    keyboard.append([
        InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_viloyatlar_shofyor"),
        InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")
    ])

    await query.message.edit_text(f"{viloyat} viloyati uchun tumanlardan birini tanlang:",
                                 reply_markup=InlineKeyboardMarkup(keyboard))


async def shofyor_elonlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, _, viloyat, tuman = query.data.split('_', 3)

    cursor.execute(
        "SELECT id, mashina, sigim, narx, telefon, premium, korilgan, sanasi, user_id FROM shofyor_elonlar WHERE viloyat = ? AND tuman = ? ORDER BY premium DESC, sanasi DESC",
        (viloyat, tuman)
    )
    elonlar = cursor.fetchall()

    if not elonlar:
        await query.message.edit_text("Bu tumanda shofyor e’lonlari mavjud emas.", reply_markup=asosiy_menu())
        return

    for elon in elonlar:
        elon_id, mashina, sigim, narx, telefon, premium, korilgan, sanasi, user_id = elon

        cursor.execute("UPDATE shofyor_elonlar SET korilgan = korilgan + 1 WHERE id = ?", (elon_id,))
        conn.commit()

        text = (
            f"🏷 E’lon ID: {elon_id}\n"
            f"📍 Manzil: {viloyat}, {tuman}\n"
            f"🚚 Mashina: {mashina}\n"
            f"⚖️ Sig‘im: {sigim}\n"
            f"💰 Narx: {narx} so‘m\n"
            f"📞 Telefon: {telefon}\n"
            f"👁 Ko‘rilgan: {korilgan + 1} marta\n"
        )

        if premium == 1:
            text = "💎 PREMIUM E'LON 💎\n\n" + text

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"📞 Raqam olish ({RAQAM_NARX} so‘m)", callback_data=f"shofyor_raqam_{elon_id}"),
            ],
            [
                InlineKeyboardButton(f"🔸 VIP e’lon — {VIP_ELON_NARX} so‘m", callback_data=f"vip_shofyor_{user_id}|{sanasi}"),
                InlineKeyboardButton(f"🌟 Super e’lon — {SUPER_ELON_NARX} so‘m", callback_data=f"super_shofyor_{user_id}|{sanasi}")
            ]
        ])

        await query.message.reply_text(text, reply_markup=keyboard)

    nav_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tumanlar_shofyor_{viloyat}")],
        [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu")]
    ])

    await query.message.reply_text("Tanlang:", reply_markup=nav_keyboard)async def orqaga_viloyatlar_shofyor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await shofyor_korish(update, context)


async def orqaga_tumanlar_shofyor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split('_')
    viloyat = parts[-1]
    await shofyor_tumanlar(update, context)


# --- E'lon muddati tugashi uchun funksiya ---
async def elon_muddat_tugashi(user_id, sanasi, context):
    await asyncio.sleep(24 * 60 * 60)  # 24 soat kutish

    cursor.execute("SELECT * FROM shofyor_elonlar WHERE user_id=? AND sanasi=?", (user_id, sanasi))
    elon = cursor.fetchone()
    if elon:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Uzaytirish", callback_data=f"uzaytir_shofyor_{user_id}|{sanasi}")],
            [InlineKeyboardButton("❌ O‘chirish", callback_data=f"ochir_shofyor_{user_id}|{sanasi}")]
        ])
        await context.bot.send_message(chat_id=user_id, text="⏳ E'loningiz muddati tugadi. Uzaytirasizmi?", reply_markup=keyboard)


# --- Uzaytirish callback ---
async def uzaytirish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_', 2)[-1]
    user_id_str, sanasi = data.split('|', 1)
    user_id = int(user_id_str)

    yangi_sana = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        UPDATE shofyor_elonlar SET sanasi=? WHERE user_id=? AND sanasi=?
    ''', (yangi_sana, user_id, sanasi))
    conn.commit()

    await query.edit_message_text("✅ E’loningiz muddati uzaytirildi.")


# --- O'chirish callback ---
async def ochirish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_', 2)[-1]
    user_id_str, sanasi = data.split('|', 1)
    user_id = int(user_id_str)

    cursor.execute('DELETE FROM shofyor_elonlar WHERE user_id=? AND sanasi=?', (user_id, sanasi))
    conn.commit()

    await query.edit_message_text("❌ E’loningiz o‘chirildi.")
