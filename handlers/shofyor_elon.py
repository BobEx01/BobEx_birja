from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database import cursor, conn
from handlers.utils import back_button
import datetime
import asyncio

# Viloyatlar tugmalari
def viloyatlar_keyboard():
    viloyatlar = ["Toshkent", "Andijon", "Farg'ona", "Namangan",
                  "Samarqand", "Buxoro", "Navoiy", "Qashqadaryo",
                  "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"]
    keyboard = [[viloyat] for viloyat in viloyatlar]
    keyboard.append(["⬅️ Orqaga"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# E’lon berish bosqichlari

async def shofyor_elon_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Viloyatni tanlang:",
        reply_markup=viloyatlar_keyboard()
    )
    return "viloyat"

async def viloyat_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await shofyor_elon_start(update, context)
    context.user_data['viloyat'] = update.message.text
    await update.message.reply_text("📍 Tumaningizni kiriting:", reply_markup=back_button())
    return "tuman"

async def tuman_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await viloyat_qabul(update, context)
    context.user_data['tuman'] = update.message.text
    await update.message.reply_text("🚗 Qanday mashinangiz bor? (Yuk sig‘imi, turi):", reply_markup=back_button())
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
    await update.message.reply_text("💵 Narxingizni kiriting (so‘m):", reply_markup=back_button())
    return "narx"

async def narx_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await sigim_qabul(update, context)
    try:
        context.user_data['narx'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❗️ Iltimos, narxni faqat raqam bilan kiriting!", reply_markup=back_button())
        return "narx"
    await update.message.reply_text("📞 Telefon raqamingizni kiriting:", reply_markup=back_button())
    return "telefon"

async def telefon_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await narx_qabul(update, context)
    context.user_data['telefon'] = update.message.text
    context.user_data['user_id'] = update.message.from_user.id
    context.user_data['sanasi'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # E'lonni saqlaymiz, premium emas (0)
    cursor.execute('''
        INSERT INTO shofyor_elonlar 
        (user_id, viloyat, tuman, mashina, sigim, narx, telefon, sanasi, premium)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        context.user_data['user_id'], context.user_data['viloyat'], context.user_data['tuman'],
        context.user_data['mashina'], context.user_data['sigim'], context.user_data['narx'],
        context.user_data['telefon'], context.user_data['sanasi'], 0
    ))
    conn.commit()

    await update.message.reply_text("✅ Shofyor e’loningiz muvaffaqiyatli joylandi!", reply_markup=ReplyKeyboardRemove())

    # Premium qilish taklifi
    await update.message.reply_text(
        "❗️ Premium e’lon qilishni xohlaysizmi? To‘lov 10,000 so‘m.\n"
        "Premium e’loningiz doimo yuqorida ko‘rsatiladi.",reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Premium qilish (10,000 so‘m)", callback_data=f"premium_{context.user_data['user_id']}_{context.user_data['sanasi']}")]
        ])
    )

    await update.message.reply_text("🏠 Bosh menyuga qaytdingiz:", reply_markup=asosiy_menu())
    return -1

# Premium callback handler
async def premium_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split('_')
    user_id, sanasi = data[1], data[2]

    cursor.execute('UPDATE shofyor_elonlar SET premium=1 WHERE user_id=? AND sanasi=?', (user_id, sanasi))
    conn.commit()

    await query.edit_message_text("✅ E’loningiz endi Premium holatga o‘tkazildi. Rahmat!")

# Shofyor e'lonlarini ko'rish uchun abonentlik tekshiruvi
async def shofyor_elonlarni_korish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute("SELECT abonentlik FROM foydalanuvchilar WHERE user_id=?", (user_id,))
    natija = cursor.fetchone()

    if natija is None or natija[0] != 1:
        # Abonentlik yo'q, to'lovni so'raymiz
        await update.message.reply_text(
            "🔒 Shofyor raqamlarini ko‘rish uchun obuna bo‘lishingiz kerak.\n"
            "Obuna narxi: 28,000 so‘m.\n\n"
            "To‘lovni amalga oshirdingizmi? (Ha/Yo‘q)",
            reply_markup=ReplyKeyboardMarkup([["Ha", "Yo‘q"], ["⬅️ Orqaga"]], resize_keyboard=True)
        )
        return "abonentlik_tasdiq"
    else:
        # Abonentlik bor, shofyor e'lonlarini ko'rsatamiz
        await shofyor_elonlarini_yuborish(update, context)
        return -1

async def abonentlik_tasdiq_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    javob = update.message.text.lower()
    user_id = update.message.from_user.id

    if javob == "⬅️ orqaga":
        return await shofyor_elonlarni_korish(update, context)
    elif javob == "ha":
        # To'lov qilingan deb hisoblaymiz va bazada abonentlik qo'shamiz
        cursor.execute("INSERT OR REPLACE INTO foydalanuvchilar (user_id, abonentlik) VALUES (?, ?)", (user_id, 1))
        conn.commit()
        await update.message.reply_text("✅ Obunangiz faollashtirildi! Endi shofyor raqamlarini ko‘rishingiz mumkin.")
        await shofyor_elonlarini_yuborish(update, context)
        return -1
    elif javob == "yo‘q":
        await update.message.reply_text("Iltimos, to‘lovni amalga oshiring yoki keyinroq qaytib keling.", reply_markup=back_button())
        return "abonentlik_tasdiq"
    else:
        await update.message.reply_text("Faqat 'Ha' yoki 'Yo‘q' deb javob bering.", reply_markup=back_button())
        return "abonentlik_tasdiq"

# Shofyor e'lonlarini yuborish (faqat abonentlar uchun telefon raqamlari bilan)
async def shofyor_elonlarini_yuborish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT viloyat, tuman, mashina, sigim, narx, telefon FROM shofyor_elonlar ORDER BY sanasi DESC LIMIT 20")
    e_olonlar = cursor.fetchall()
    if not e_olonlar:
        await update.message.reply_text("Shofyor e’lonlari topilmadi.")
        return
    text = "📢 Shofyor e’lonlari:\n\n"
    for e in e_olonlar:
        viloyat, tuman, mashina, sigim, narx, telefon = e
        text += (f"📍 {viloyat}, {tuman}\n"
                 f"🚗
