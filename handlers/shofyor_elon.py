from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database import cursor, conn, foydalanuvchi_mavjudmi
from config import VIP_ELON_NARX, SUPER_ELON_NARX, ADMIN_ID
from handlers.start import asosiy_menu
import datetime
import asyncio


def viloyatlar_keyboard():
    viloyatlar = ["Toshkent", "Andijon", "Farg'ona", "Namangan",
                  "Samarqand", "Buxoro", "Navoiy", "Qashqadaryo",
                  "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"]
    keyboard = [[v] for v in viloyatlar]
    keyboard.append(["⬅️ Orqaga"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def back_button():
    return ReplyKeyboardMarkup([["⬅️ Orqaga"]], resize_keyboard=True)


async def shofyor_elon_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 Viloyatni tanlang:", reply_markup=viloyatlar_keyboard())
    return "viloyat"


async def viloyat_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        await update.message.reply_text("🏠 Bosh menyu:", reply_markup=asosiy_menu())
        return -1

    context.user_data['viloyat'] = update.message.text
    await update.message.reply_text("📍 Tumaningizni kiriting:", reply_markup=back_button())
    return "tuman"


async def tuman_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await shofyor_elon_start(update, context)

    context.user_data['tuman'] = update.message.text
    await update.message.reply_text("🚗 Qanday mashinangiz bor?", reply_markup=back_button())
    return "mashina"


async def mashina_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await tuman_qabul(update, context)

    context.user_data['mashina'] = update.message.text
    await update.message.reply_text("⚖️ Mashina sig‘imini kiriting (kg yoki tonna):", reply_markup=back_button())
    return "sigim"


async def sigim_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await mashina_qabul(update, context)

    context.user_data['sigim'] = update.message.text
    await update.message.reply_text("💰 Narxingizni kiriting (so‘m):", reply_markup=back_button())
    return "narx"


async def narx_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await sigim_qabul(update, context)

    try:
        context.user_data['narx'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❗️ Iltimos, faqat raqam kiriting!", reply_markup=back_button())
        return "narx"

    await update.message.reply_text("📞 Telefon raqamingizni kiriting:", reply_markup=back_button())
    return "telefon"


async def telefon_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await narx_qabul(update, context)

    user_id = update.message.from_user.id
    context.user_data['telefon'] = update.message.text
    sanasi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not foydalanuvchi_mavjudmi(user_id):
        cursor.execute("INSERT INTO foydalanuvchilar (user_id, balans, sarflangan) VALUES (?, 0, 0)", (user_id,))
        conn.commit()

    cursor.execute('''
        INSERT INTO shofyor_elonlar
        (user_id, viloyat, tuman, mashina, sigim, narx, telefon, sanasi, premium)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
    ''', (
        user_id,
        context.user_data['viloyat'],
        context.user_data['tuman'],
        context.user_data['mashina'],
        context.user_data['sigim'],
        context.user_data['narx'],
        context.user_data['telefon'],
        sanasi
    ))
    conn.commit()

    await update.message.reply_text("✅ Shofyor e’loningiz muvaffaqiyatli joylandi!", reply_markup=ReplyKeyboardRemove())await update.message.reply_text(
        "🔝 E’loningizni yanada samarali qilishni xohlaysizmi?\nQuyidagilardan birini tanlang:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🔸 VIP e’lon — {VIP_ELON_NARX} so‘m", callback_data=f"vip_shofyor_{user_id}|{sanasi}")],
            [InlineKeyboardButton(f"🌟 Super e’lon — {SUPER_ELON_NARX} so‘m", callback_data=f"super_shofyor_{user_id}|{sanasi}")]
        ])
    )

    asyncio.create_task(elon_muddat_tugashi(user_id, sanasi, context))

    await update.message.reply_text("🏠 Bosh menyuga qaytdingiz:", reply_markup=asosiy_menu())
    return -1


async def elon_muddat_tugashi(user_id, sanasi, context):
    await asyncio.sleep(24 * 60 * 60)

    cursor.execute("SELECT * FROM shofyor_elonlar WHERE user_id=? AND sanasi=?", (user_id, sanasi))
    elon = cursor.fetchone()
    if elon:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Uzaytirish", callback_data=f"uzaytir_shofyor_{user_id}|{sanasi}")],
            [InlineKeyboardButton("❌ O‘chirish", callback_data=f"ochir_shofyor_{user_id}|{sanasi}")]
        ])
        await context.bot.send_message(chat_id=user_id, text="⏳ E'loningiz muddati tugadi. Uzaytirasizmi?", reply_markup=keyboard)


async def uzaytirish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_', 2)[-1]
    user_id_str, sanasi = data.split('|', 1)
    user_id = int(user_id_str)

    cursor.execute('''
        UPDATE shofyor_elonlar SET sanasi=? WHERE user_id=? AND sanasi=?
    ''', (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, sanasi))
    conn.commit()

    await query.edit_message_text("✅ E’loningiz muddati uzaytirildi.")


async def ochirish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_', 2)[-1]
    user_id_str, sanasi = data.split('|', 1)
    user_id = int(user_id_str)

    cursor.execute('''
        DELETE FROM shofyor_elonlar WHERE user_id=? AND sanasi=?
    ''', (user_id, sanasi))
    conn.commit()

    await query.edit_message_text("❌ E’loningiz o‘chirildi.")


async def vip_shofyor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await elon_upgrade_callback(update, context, 'VIP', VIP_ELON_NARX, bonus=1)


async def super_shofyor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await elon_upgrade_callback(update, context, 'SUPER', SUPER_ELON_NARX, bonus=3)


async def elon_upgrade_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, tur, narx, bonus):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')[-1]
    user_id_str, sanasi = data.split('|', 1)
    user_id = int(user_id_str)

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    if not result:
        await query.edit_message_text("❌ Balansingiz topilmadi. Avval balansni to‘ldiring.")
        return

    balans = result[0]
    if balans < narx:
        await query.edit_message_text("❌ Balansingiz yetarli emas. Iltimos, balansingizni to‘ldiring.")
        return

    cursor.execute('''
        UPDATE foydalanuvchilar
        SET balans = balans - ?, sarflangan = sarflangan + ?
        WHERE user_id=?
    ''', (narx, narx, user_id))

    cursor.execute('''
        UPDATE shofyor_elonlar
        SET premium = 1
        WHERE user_id=? AND sanasi=?
    ''', (user_id, sanasi))

    conn.commit()

    await query.edit_message_text(f"✅ E’loningiz {tur} holatga ko‘tarildi.\nBonus: {bonus} ta telefon raqam bepul olish huquqi berildi!")
    await context.bot.send_message(ADMIN_ID, f"📢 User {user_id} shofyor e’loni uchun {tur} sotib oldi.")
