from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from database import cursor, conn
from handlers.start import asosiy_menu

ADMIN_ID = 8080091052

# Bosqichlar
TOLOV_MIqdori, TOLOV_CHEK = range(2)

async def hisobim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Balansni olish
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    balans = result[0] if result else 0

    text = f"💳 Hisobingiz: {balans} so'm\n\nHisobingizni to‘ldirish uchun «Hisobni to‘ldirish» tugmasini bosing."
    keyboard = [["Hisobni to‘ldirish"], ["⬅️ Orqaga"]]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def hisobni_tolidirish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💳 Hisobni to‘ldirish bo‘limi:\n\n"
        "To'lov tizimi: 🔷 Humo[Card]\n"
        "Hamyon: 5614 6822 1820 6250\n"
        "ID: {user_id}\n\n"
        "🔹 Minimal: 10,000 so'm\n"
        "🔹 Maksimal: 10,000,000 so'm\n\n"
        "Karta raqam egasi:  Muhammadbobur.A\n\n"
        "Hisobni to'ldirish uchun quyidagilarni bajaring:\n"
        "1) Hamyonga pul o‘tkazing.\n"
        "2) «✅ To‘lov qildim» tugmasini bosing.\n"
        "3) Tashlagan pul miqdorini kiriting.\n"
        "4) To‘lov chek rasmini yuboring.\n"
        "5) Admin tasdiqlashini kuting.\n\n"
        "⚠️ To‘lovingiz 15-500 daqiqa ichida ko‘rib chiqiladi.\n"
        "Bot orqali kiritilgan pul qaytarilmaydi — faqat xizmat uchun."
    ).format(user_id=update.message.from_user.id)

    keyboard = [["✅ To‘lov qildim"], ["⬅️ Orqaga"]]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return TOLOV_MIqdori

async def tolov_miqdori_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tolov_miqdori'] = update.message.text
    await update.message.reply_text("📸 Endi to‘lov chek rasmini yuboring:")
    return TOLOV_CHEK

async def tolov_chek_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    miqdor = context.user_data.get('tolov_miqdori')
    photo = update.message.photo[-1].file_id if update.message.photo else None

    if photo:
        await update.message.reply_text("✅ To‘lovingiz qabul qilindi. Admin tekshiradi.", reply_markup=asosiy_menu())

        # Adminga habar
        text = (
            f"💵 Yangi to‘lov!\n\n"
            f"👤 User ID: {user_id}\n"
            f"💰 Miqdor: {miqdor} so‘m\n"
            f"✅ Tasdiqlash uchun: /tasdiqla_{user_id}_{miqdor}"
        )
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=text
        )
    else:
        await update.message.reply_text("❗️ Chek rasmi topilmadi, qaytadan urinib ko‘ring.")

    return ConversationHandler.END

async def admin_tasdiqlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = update.message.text.split('_')
    if len(args) != 3:
        await update.message.reply_text("❗️ Noto‘g‘ri format.")
        return

    _, user_id, miqdor = args
    user_id = int(user_id)
    miqdor = int(miqdor)

    # Balansni yangilash
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        yangi_balans = result[0] + miqdor
        cursor.execute("UPDATE foydalanuvchilar SET balans = ? WHERE user_id = ?", (yangi_balans, user_id))
        conn.commit()

        # Userga habar
        await context.bot.send_message(chat_id=user_id, text=f"✅ To‘lovingiz admin tomonidan tasdiqlandi. Balansingiz: {yangi_balans} so'm.")
        await update.message.reply_text("✅ Foydalanuvchi balansi yangilandi.")
    else:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")


async def ortga_qaytish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 Bosh menyu:", reply_markup=asosiy_menu())
    return ConversationHandler.END
