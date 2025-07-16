from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes
from database import cursor, conn
import datetime

# 📌 Viloyatlar tugmasi
def viloyatlar_keyboard():
    viloyatlar = ["Toshkent", "Andijon", "Farg'ona", "Namangan",
                  "Samarqand", "Buxoro", "Navoiy", "Qashqadaryo",
                  "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"]
    keyboard = [[viloyat] for viloyat in viloyatlar]
    keyboard.append(["⬅️ Orqaga"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 📌 Orqaga tugmasi
def back_button():
    return ReplyKeyboardMarkup([["⬅️ Orqaga"]], resize_keyboard=True)

# 📌 Asosiy menyu
def main_menu_keyboard():
    keyboard = [
        ["➕ Yuk joylash", "🚚 Yuklarni ko‘rish"],
        ["➕ Shofyor e'lon joylash", "🚗 Shofyorlarni ko‘rish"],
        ["🔎 Shofyor kerak", "🔍 Yuk kerak"],
        ["📞 Aloqa", "ℹ️ Ma’lumot"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ➡️ 1. Boshlash
async def yuk_elon_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 Viloyatni tanlang:",
        reply_markup=viloyatlar_keyboard()
    )
    return "viloyat"

# ➡️ 2. Viloyat qabul qilish
async def viloyat_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await yuk_elon_start(update, context)

    context.user_data['viloyat'] = update.message.text
    await update.message.reply_text("📍 Tumaningizni kiriting:", reply_markup=back_button())
    return "tuman"

# ➡️ 3. Tuman qabul qilish
async def tuman_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await viloyat_qabul(update, context)

    context.user_data['tuman'] = update.message.text
    await update.message.reply_text("🚩 Yuk qayerdan jo‘natiladi?", reply_markup=back_button())
    return "qayerdan"

# ➡️ 4. Qayerdan qabul qilish
async def qayerdan_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await tuman_qabul(update, context)

    context.user_data['qayerdan'] = update.message.text
    await update.message.reply_text("🚩 Yuk qayerga boradi?", reply_markup=back_button())
    return "qayerga"

# ➡️ 5. Qayerga qabul qilish
async def qayerga_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await qayerdan_qabul(update, context)

    context.user_data['qayerga'] = update.message.text
    await update.message.reply_text("⚖️ Yuk og‘irligini kiriting (kg yoki tonna):", reply_markup=back_button())
    return "ogirlik"

# ➡️ 6. Og‘irlik qabul qilish
async def ogirlik_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await qayerga_qabul(update, context)

    context.user_data['ogirlik'] = update.message.text
    await update.message.reply_text("🚚 Qanday mashina kerak?", reply_markup=back_button())
    return "mashina"

# ➡️ 7. Mashina turi
async def mashina_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await ogirlik_qabul(update, context)

    context.user_data['mashina'] = update.message.text
    await update.message.reply_text("💵 Shofyor uchun to‘lov miqdorini kiriting (so‘m):", reply_markup=back_button())
    return "narx"

# ➡️ 8. Narx qabul qilish
async def narx_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await mashina_qabul(update, context)

    try:
        context.user_data['narx'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❗️ Iltimos, to‘lovni faqat raqam bilan kiriting!", reply_markup=back_button())
        return "narx"

    await update.message.reply_text("📞 Telefon raqamingizni kiriting:", reply_markup=back_button())
    return "telefon"

# ➡️ 9.
Telefon raqam va saqlash
async def telefon_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "⬅️ Orqaga":
        return await narx_qabul(update, context)

    context.user_data['telefon'] = update.message.text
    context.user_data['user_id'] = update.message.from_user.id
    context.user_data['sanasi'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO yuk_elonlar 
        (user_id, viloyat, tuman, qayerdan, qayerga, ogirlik, mashina, narx, telefon, sanasi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        context.user_data['user_id'],
        context.user_data['viloyat'],
        context.user_data['tuman'],
        context.user_data['qayerdan'],
        context.user_data['qayerga'],
        context.user_data['ogirlik'],
        context.user_data['mashina'],
        context.user_data['narx'],
        context.user_data['telefon'],
        context.user_data['sanasi']
    ))
    conn.commit()

    await update.message.reply_text(
        "✅ Yuk e’loningiz muvaffaqiyatli joylandi!",
        reply_markup=ReplyKeyboardRemove()
    )

    await update.message.reply_text(
        "🏠 Bosh menyuga qaytdingiz. Quyidagilardan birini tanlang:",
        reply_markup=main_menu_keyboard()
    )

    return -1  # Conversation tugaydi
