from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from handlers.start import asosiy_menu

TOLOV_MIqdori, TOLOV_CHEK = range(2)

ADMIN_ID = 8080091052  # Admin user ID

async def hisobni_tolidirish_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💵 To‘lov miqdorini kiriting (so'm):",
        reply_markup=ReplyKeyboardMarkup([["⬅️ Orqaga"]], resize_keyboard=True)
    )
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
        text = (
            f"💵 Yangi to‘lov:\n\n"
            f"👤 User ID: {user_id}\n"
            f"💰 Miqdor: {miqdor} so‘m\n"
            f"✅ Tasdiqlash uchun: /tasdiqla_{user_id}_{miqdor}"
        )
        await update.message.reply_text("✅ To‘lovingiz qabul qilindi. Admin tasdiqlaydi.", reply_markup=asosiy_menu())

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=text
        )
    else:
        await update.message.reply_text("❗️ Chek rasmi topilmadi, qayta yuboring.")
        return TOLOV_CHEK

    return ConversationHandler.END

async def ortga_qaytish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 Bosh menyu:", reply_markup=asosiy_menu())
    return ConversationHandler.END
