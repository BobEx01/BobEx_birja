# handlers/shofyor_elon.py

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import datetime
import asyncio
from database import cursor, conn
from config import VIP_ELON_NARX, SUPER_ELON_NARX
from handlers.start import asosiy_menu

def viloyatlar_keyboard():
    viloyatlar = ["Toshkent", "Andijon", "Farg'ona", "Namangan",
                  "Samarqand", "Buxoro", "Navoiy", "Qashqadaryo",
                  "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"]
    keyboard = [[viloyat] for viloyat in viloyatlar]
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
        await update.message.reply_text("❗️ Faqat raqam kiriting!", reply_markup=back_button())
        return "narx"

    await update.message.reply_text("📞 Telefon raqamingizni kiriting:", reply_markup=back_button())
    return "telefon"

async def telefon_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await narx_qabul(update, context)

    user_id = update.message.from_user.id
    sanasi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        update.message.text,
        sanasi
    ))
    conn.commit()

    await update.message.reply_text("✅ Shofyor e’loningiz joylandi!", reply_markup=ReplyKeyboardRemove())

    await update.message.reply_text(
        f"🔝 E’loningizni VIP yoki Super qilishni xohlaysizmi?\n\n"
        f"🔸 VIP E'lon — {VIP_ELON_NARX} so'm\n"
        f"🌟 Super E'lon — {SUPER_ELON_NARX} so'm\n\n"
        "Kerakli tugmani tanlang:",reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔸 VIP E’lon qilish", callback_data=f"vip_elon_{user_id}|{sanasi}")],
            [InlineKeyboardButton("🌟 Super E’lon qilish", callback_data=f"super_elon_{user_id}|{sanasi}")]
        ])
    )

    asyncio.create_task(elon_muddat_tugashi(user_id, sanasi, context))

    await update.message.reply_text("🏠 Bosh menyuga qaytdingiz:", reply_markup=asosiy_menu())
    return -1

async def elon_muddat_tugashi(user_id, sanasi, context):
    await asyncio.sleep(24*60*60)

    cursor.execute("SELECT id FROM shofyor_elonlar WHERE user_id=? AND sanasi=?", (user_id, sanasi))
    elon = cursor.fetchone()

    if elon:
        await context.bot.send_message(
            chat_id=user_id,
            text="⏰ Shofyor e’loningiz muddati tugadi. Qanday amal qilamiz?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Uzaytirish", callback_data=f"shofyor_uzaytir_{elon[0]}")],
                [InlineKeyboardButton("🗑 O‘chirish", callback_data=f"shofyor_ochir_{elon[0]}")]
            ])
        )

async def shofyor_ochir_qoldir_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    amal, elon_id = data[1], int(data[2])

    if amal == 'ochir':
        cursor.execute("DELETE FROM shofyor_elonlar WHERE id=?", (elon_id,))
        conn.commit()
        await query.edit_message_text("🗑 E’lon o‘chirildi.")
    elif amal == 'uzaytir':
        cursor.execute('''
            UPDATE shofyor_elonlar SET sanasi=?
            WHERE id=?
        ''', (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), elon_id))
        conn.commit()
        await query.edit_message_text("✅ E’lon muddati uzaytirildi.")
