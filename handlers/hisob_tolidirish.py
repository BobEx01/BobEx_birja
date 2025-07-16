from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import cursor, conn
from handlers.start import asosiy_menu

ADMIN_ID = 8080091052

TOLOV_MIqdori, TOLOV_CHEK = range(2)


async def hisobni_tolidirish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = (
        f"💳 *Hisobni to‘ldirish uchun karta rekvizitlari:*\n\n"
        "🔹 *Uzcard / Humo:* 5614 6822 1820 6250\n\n"
        f"🆔 *Foydalanuvchi ID:* `{user_id}`\n\n"
        "🔹 *Minimal:* 10,000 so'm\n"
        "🔹 *Maksimal:* 10,000,000 so'm\n\n"
        "*Karta egasi:* Muhammadbobur.A\n\n"
        "1️⃣ Pul o'tkazing\n"
        "2️⃣ «✅ To‘lov qildim» tugmasini bosing\n\n"
        "_⚠️ To‘langan pul faqat xizmatlar uchun sarflanadi va qaytarib berilmaydi!_"
    )
    keyboard = [["✅ To‘lov qildim"], ["⬅️ Orqaga"]]
    await update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True), parse_mode="Markdown")
    return TOLOV_MIqdori


async def tolov_miqdori_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        miqdor = int(update.message.text)
        if miqdor < 10000:
            await update.message.reply_text("❗️ Minimal to‘lov miqdori 10,000 so'm. Qayta kiriting.")
            return TOLOV_MIqdori
    except ValueError:
        await update.message.reply_text("❗️ Iltimos, to‘lov miqdorini faqat raqamda kiriting.")
        return TOLOV_MIqdori

    context.user_data['tolov_miqdori'] = miqdor
    await update.message.reply_text("📸 Endi to‘lov chek rasmini yuboring:")
    return TOLOV_CHEK


async def tolov_chek_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    miqdor = context.user_data.get('tolov_miqdori')
    photo = update.message.photo[-1].file_id if update.message.photo else None

    if photo:
        await update.message.reply_text("✅ To‘lovingiz qabul qilindi. Admin tasdiqlaydi.", reply_markup=asosiy_menu())

        text = (
            f"💵 *Yangi to‘lov kelib tushdi!*\n\n"
            f"👤 *User ID:* `{user_id}`\n"
            f"💰 *Miqdor:* {miqdor} so‘m\n\n"
            f"✅ Tasdiqlash uchun: `/tasdiqla_{user_id}_{miqdor}`\n\n"
            "_Eslatma: To‘langan pul faqat xizmatlar uchun sarflanadi va qaytarilmaydi!_"
        )
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=text,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❗️ Chek rasmi topilmadi. Iltimos, qayta yuboring.")
        return TOLOV_CHEK

    return ConversationHandler.END


async def admin_tasdiqlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = update.message.text.split('_')
    if len(args) != 3:
        await update.message.reply_text("❗️ Noto‘g‘ri format. /tasdiqla_USERID_MIqdor")
        return

    _, user_id, miqdor = args
    user_id = int(user_id)
    miqdor = int(miqdor)

    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        yangi_balans = result[0] + miqdor
        cursor.execute("UPDATE foydalanuvchilar SET balans = ? WHERE user_id = ?", (yangi_balans, user_id))
        conn.commit()

        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ To‘lovingiz admin tomonidan tasdiqlandi.\n\nYangi balans: {yangi_balans} so'm.\n\n"
                 "Bu balans faqat xizmatlar uchun sarflanishi mumkin va qaytarilmaydi."
        )
        await update.message.reply_text(f"✅ User {user_id} balansiga {miqdor} so‘m qo‘shildi. Yangi balans: {yangi_balans} so'm.")
    else:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")


async def ortga_qaytish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 Bosh menyu:", reply_markup=asosiy_menu())
    return ConversationHandler.END
