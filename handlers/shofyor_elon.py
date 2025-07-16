from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
from database import cursor, conn
import datetime
import asyncio

# Foydalanuvchi ma'lumotlarini saqlash uchun lug'at
user_data = {}

def viloyatlar_keyboard():
    viloyatlar = [
        "Toshkent", "Andijon", "Farg'ona", "Namangan",
        "Samarqand", "Buxoro", "Navoiy", "Qashqadaryo",
        "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"
    ]
    keyboard = [[v] for v in viloyatlar]
    keyboard.append(["⬅️ Orqaga"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def back_button():
    return ReplyKeyboardMarkup([["⬅️ Orqaga"]], resize_keyboard=True)

def main_menu_keyboard():
    keyboard = [
        ["🚛 Yuk uchun e'lon berish"],
        ["🚚 Shofyor e'lon berish"],
        ["📦 Yuk e'lonlarini ko‘rish"],
        ["🚚 Shofyor e'lonlarini ko‘rish"],
        ["💳 Hisobim"],
        ["🎁 Paketlar"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# E'lon berishni boshlash
async def shofyor_elon_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Viloyatni tanlang:",
        reply_markup=viloyatlar_keyboard()
    )
    return "viloyat"

async def viloyat_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        # Orqaga bosinganda asosiy menyuga qaytish mumkin
        await update.message.reply_text(
            "🏠 Bosh menyu",
            reply_markup=main_menu_keyboard()
        )
        return -1

    user_data['viloyat'] = update.message.text
    await update.message.reply_text(
        "📍 Tumaningizni kiriting:",
        reply_markup=back_button()
    )
    return "tuman"

async def tuman_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await shofyor_elon_start(update, context)

    user_data['tuman'] = update.message.text
    await update.message.reply_text(
        "🚗 Qanday mashinangiz bor? (Yuk sig‘imi, turi)",
        reply_markup=back_button()
    )
    return "mashina"

async def mashina_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await tuman_qabul(update, context)

    user_data['mashina'] = update.message.text
    await update.message.reply_text(
        "⚖️ Mashina sig‘imini kiriting (kg yoki tonna):",
        reply_markup=back_button()
    )
    return "sigim"

async def sigim_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await mashina_qabul(update, context)

    user_data['sigim'] = update.message.text
    await update.message.reply_text(
        "💰 Narxingizni kiriting (so‘m):",
        reply_markup=back_button()
    )
    return "narx"

async def narx_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await sigim_qabul(update, context)

    try:
        user_data['narx'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text(
            "❗️ Iltimos, narxni faqat raqam bilan kiriting!",
            reply_markup=back_button()
        )
        return "narx"

    await update.message.reply_text(
        "📞 Telefon raqamingizni kiriting:",
        reply_markup=back_button()
    )
    return "telefon"

async def telefon_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await narx_qabul(update, context)

    user_data['telefon'] = update.message.text
    user_data['user_id'] = update.message.from_user.id
    user_data['sanasi'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # E'lonni bazaga yozish (premium = 0 - bepul)
    cursor.execute('''
        INSERT INTO shofyor_elonlar
        (user_id, viloyat, tuman, mashina, sigim, narx, telefon, sanasi, premium)VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
    ''', (
        user_data['user_id'], user_data['viloyat'], user_data['tuman'],
        user_data['mashina'], user_data['sigim'], user_data['narx'],
        user_data['telefon'], user_data['sanasi']
    ))
    conn.commit()

    # Premium taklifini yuborish
    await update.message.reply_text(
        "✅ Shofyor e’loningiz muvaffaqiyatli joylandi!\n\n"
        "❗️ Premium e’lon qilishni xohlaysizmi? To‘lov 10,000 so‘m.\n"
        "Premium e’loningiz doimo yuqorida ko‘rsatiladi.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Premium qilish (10,000 so‘m)", callback_data=f"premium_{user_data['user_id']}_{user_data['sanasi']}")]
        ])
    )

    # 24 soatlik e'lon muddati monitoringi
    asyncio.create_task(elon_muddat_tugashi(user_data['user_id'], user_data['sanasi'], context))

    await update.message.reply_text(
        "🏠 Bosh menyuga qaytdingiz:",
        reply_markup=main_menu_keyboard()
    )
    return -1


# Premium qilish callback
async def premium_qilish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    user_id, sanasi = data[1], data[2]

    cursor.execute(
        'UPDATE shofyor_elonlar SET premium=1 WHERE user_id=? AND sanasi=?',
        (user_id, sanasi)
    )
    conn.commit()

    await query.edit_message_text("✅ E’loningiz endi Premium holatga o‘tkazildi. Rahmat!")


# Shofyor raqamlarini faqat abonent to‘lovi qilinganlarga ko‘rsatish
async def shofyor_raqamlarini_yuborish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Foydalanuvchi abonentligi va to'lovi tekshiruvi (28.000 so'm)
    cursor.execute(
        "SELECT tolov_miqdori, tolov_sana FROM abonentlar WHERE user_id=? ORDER BY tolov_sana DESC LIMIT 1",
        (user_id,)
    )
    abonent = cursor.fetchone()
    hozirgi_sana = datetime.datetime.now()

    if abonent:
        tolov_miqdori, tolov_sana = abonent
        tolov_sana_dt = datetime.datetime.strptime(tolov_sana, "%Y-%m-%d %H:%M:%S")
        # 30 kun davomida abonent bo'lish sharti
        if tolov_miqdori >= 28000 and (hozirgi_sana - tolov_sana_dt).days <= 30:
            # To'lov muddati hali o'tmagan - raqamlarni ko'rsatish
            await shofyor_raqamlarini_yuborish_haqiqat(update, context)
            return
    # Agar abonent bo'lmasa yoki to'lov muddati o'tgan bo'lsa:
    await update.message.reply_text(
        "❌ Siz shofyorlarning telefon raqamlarini ko‘rish uchun 28,000 so‘m to‘lashingiz kerak.\n"
        "To‘lov uchun /tolov buyrug‘ini bosing."
    )


async def shofyor_raqamlarini_yuborish_haqiqat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute(
        "SELECT viloyat, tuman, mashina, sigim, narx, telefon FROM shofyor_elonlar WHERE premium=1 ORDER BY sanasi DESC LIMIT 20"
    )
    elonlar = cursor.fetchall()
    if not elonlar:
        await update.message.reply_text("Shofyor e’lonlari topilmadi.")
        return

    text = "📢 Premium Shofyor e’lonlari:\n\n"
    for e in elonlar:
        viloyat, tuman, mashina, sigim, narx, telefon = e
        text += (
            f"📍 {viloyat}, {tuman}\n"
            f"🚗 {mashina}\n"
            f"⚖️ Sig‘im: {sigim}\n"
            f"💰 Narx: {narx} so‘m\n"
            f"📞 Telefon: {telefon}\n\n"
        )
    await update.message.reply_text(text)


# 24 soatlik e'lon muddati tugashi uchun kuzatuv
async def elon_muddat_tugashi(user_id, sanasi, context):
    await asyncio.sleep(24 * 60 * 60)  # 24 soat

    cursor.execute(
        "SELECT * FROM shofyor_elonlar WHERE user_id=? AND sanasi=?",
        (user_id, sanasi)
    )
    elon = cursor.fetchone()
    if elon:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Uzaytirish", callback_data=f"uzaytir_{user_id}_{sanasi}")],
            [InlineKeyboardButton("❌ O‘chirish", callback_data=f"ochir_{user_id}_{sanasi}")]
        ])
        await context.bot.send_message(chat_id=user_id,
            text="⏳ E'loningiz muddati tugadi. Uzaytirasizmi?",
            reply_markup=keyboard
        )

        await asyncio.sleep(8 * 60 * 60)  # 8 soat

        cursor.execute(
            "SELECT * FROM shofyor_elonlar WHERE user_id=? AND sanasi=?",
            (user_id, sanasi)
        )
        check = cursor.fetchone()
        if check:
            cursor.execute(
                "DELETE FROM shofyor_elonlar WHERE user_id=? AND sanasi=?",
                (user_id, sanasi)
            )
            conn.commit()
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ E'loningiz o‘chirildi."
            )


# Callback uchun uzaytirish
async def uzaytirish_callback(update:
