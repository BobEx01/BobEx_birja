from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# VIP E'lon funksiyasi
async def vip_elon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✨ *VIP E'lon Xizmati* ✨\n\n"
        "🔝 VIP e'loningiz doimo oddiy e'lonlar ustida ko‘rinadi va ko‘proq ko‘rinish oladi.\n\n"
        "💵 *Narxi:* 45,000 so'm\n"
        "⏳ *Muddat:* 24 soat\n"
        "🎁 *Bonus:* 1 marta telefon raqam olish imkoniyati\n\n"
        "To‘lov qilish uchun quyidagi tugmani bosing 👇"
    )

    buttons = [
        [InlineKeyboardButton("💳 VIP E'lon uchun to‘lash - 45,000 so'm", callback_data='vip_tolov')],
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode='Markdown'
    )

# Super E'lon funksiyasi
async def super_elon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 *SUPER E'lon Xizmati* 🚀\n\n"
        "👑 Super e'lon - barcha e'lonlarning eng yuqorisida joylashadi va *SUPER* belgisi bilan ajralib turadi.\n\n"
        "💵 *Narxi:* 90,000 so'm\n"
        "⏳ *Muddat:* 24 soat\n"
        "🎁 *Bonus:* 3 marta telefon raqam olish imkoniyati\n\n"
        "To‘lov qilish uchun quyidagi tugmani bosing 👇"
    )

    buttons = [
        [InlineKeyboardButton("💳 Super E'lon uchun to‘lash - 90,000 so'm", callback_data='super_tolov')],
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode='Markdown'
    )

# VIP aktiv funksiyasi
async def vip_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ *VIP E'loningiz faollashtirildi!*\n"
        "🕐 Amal qilish muddati: 24 soat\n"
        "🎁 Bonus: 1 marta telefon raqam olish huquqi\n"
        "📌 E'loningiz yuqorida joylashadi.",
        parse_mode='Markdown'
    )

# Super aktiv funksiyasi
async def super_aktiv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ *Super E'loningiz faollashtirildi!*\n"
        "🕐 Amal qilish muddati: 24 soat\n"
        "🎁 Bonus: 3 marta telefon raqam olish huquqi\n"
        "🚀 E'loningiz barcha e'lonlardan yuqorida ko‘rsatiladi.",
        parse_mode='Markdown'
    )

# --- QUYIDAGI IKKITA CALLBACK FUNKSIYA main.py uchun xato chiqmasligi uchun ---
async def vip_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "✅ *VIP E'lon aktivlashtirildi!*\n\n"
        "⏰ Muddat: 24 soat\n"
        "🎁 Bonus: 1 marta raqam olish imkoniyati.",
        parse_mode='Markdown'
    )

async def super_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "✅ *Super E'lon aktivlashtirildi!*\n\n"
        "⏰ Muddat: 24 soat\n"
        "🎁 Bonus: 3 marta raqam olish imkoniyati.",
        parse_mode='Markdown'
    )
