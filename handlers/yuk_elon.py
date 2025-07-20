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


async def yuk_elon_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 Viloyatni tanlang:", reply_markup=viloyatlar_keyboard())
    return "viloyat"


async def viloyat_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await yuk_elon_start(update, context)

    context.user_data['viloyat'] = update.message.text
    await update.message.reply_text("📍 Tumaningizni kiriting:", reply_markup=back_button())
    return "tuman"


async def tuman_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await viloyat_qabul(update, context)

    context.user_data['tuman'] = update.message.text
    await update.message.reply_text("🚩 Yuk qayerdan jo‘natiladi?", reply_markup=back_button())
    return "qayerdan"


async def qayerdan_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await tuman_qabul(update, context)

    context.user_data['qayerdan'] = update.message.text
    await update.message.reply_text("🚩 Yuk qayerga boradi?", reply_markup=back_button())
    return "qayerga"


async def qayerga_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await qayerdan_qabul(update, context)

    context.user_data['qayerga'] = update.message.text
    await update.message.reply_text("⚖️ Yuk og‘irligini kiriting (kg yoki tonna):", reply_markup=back_button())
    return "ogirlik"


async def ogirlik_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await qayerga_qabul(update, context)

    context.user_data['ogirlik'] = update.message.text
    await update.message.reply_text("🚚 Qanday mashina kerak?", reply_markup=back_button())
    return "mashina"


async def mashina_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await ogirlik_qabul(update, context)

    context.user_data['mashina'] = update.message.text
    await update.message.reply_text("💵 Shofyor uchun to‘lov miqdorini kiriting (so‘m):", reply_markup=back_button())
    return "narx"


async def narx_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await mashina_qabul(update, context)

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

    context.user_data['telefon'] = update.message.text
    user_id = update.message.from_user.id
    sanasi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    muddat = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''INSERT INTO yuk_elonlar (user_id, viloyat, tuman, qayerdan, qayerga, ogirlik, mashina, narx, telefon, sanasi, muddat, premium)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    ''', (
        user_id,
        context.user_data['viloyat'],
        context.user_data['tuman'],
        context.user_data['qayerdan'],
        context.user_data['qayerga'],
        context.user_data['ogirlik'],
        context.user_data['mashina'],
        context.user_data['narx'],
        context.user_data['telefon'],
        sanasi,
        muddat
    ))
    conn.commit()

    await update.message.reply_text(
        "✅ Yuk e’loningiz muvaffaqiyatli joylandi!\n\n"
        "❗️ E’loningizni ko‘proq odam ko‘rishi uchun VIP yoki Super E'lon qilib faollashtiring:\n\n"
        f"🔸 VIP E'lon — {VIP_ELON_NARX} so'm, 24 soat davomida ustunlik + 1 ta telefon raqam olish bonus.\n"
        f"🌟 Super E'lon — {SUPER_ELON_NARX} so'm, barcha e'lonlardan yuqorida + 3 ta raqam olish bonus.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔸 VIP E’lon qilish", callback_data=f"vip_yuk_{user_id}|{sanasi}")],
            [InlineKeyboardButton("🌟 Super E’lon qilish", callback_data=f"super_yuk_{user_id}|{sanasi}")]
        ]),
        parse_mode='Markdown'
    )

    asyncio.create_task(elon_muddat_tugashi(user_id, sanasi, context))

    await update.message.reply_text("🏠 Bosh menyuga qaytdingiz:", reply_markup=asosiy_menu())
    return -1


async def elon_muddat_tugashi(user_id, sanasi, context):
    await asyncio.sleep(24 * 60 * 60)
    cursor.execute("SELECT id FROM yuk_elonlar WHERE user_id=? AND sanasi=?", (user_id, sanasi))
    elon = cursor.fetchone()
    if elon:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🗑 O‘chirish", callback_data=f"yuk_ochir_yuk_{elon[0]}")],
            [InlineKeyboardButton("✅ Qoldirish", callback_data=f"yuk_qoldir_yuk_{elon[0]}")]
        ])
        await context.bot.send_message(
            chat_id=user_id,
            text="⏰ E’loningiz muddati tugadi. Yangi mijozlar bo‘lishi uchun uzaytiring yoki o‘chirib yuboring.",
            reply_markup=keyboard
        )


async def yuk_ochir_qoldir_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    amal, elon_turi, elon_id = data[1], data[2], int(data[3])

    if amal == 'ochir':
        if elon_turi == 'yuk':
            cursor.execute("DELETE FROM yuk_elonlar WHERE id=?", (elon_id,))
            await query.edit_message_text("🗑 E’loningiz o‘chirildi.")
    elif amal == 'qoldir':
        await query.edit_message_text("✅ E’loningiz qoldirildi va hali ham ko‘rsatilmoqda.")

    conn.commit()
