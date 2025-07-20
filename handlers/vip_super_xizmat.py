from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Bonus paket qo'shish funksiyasi (bazaga moslab o'zgartiring)
async def bonus_paket_qoshish(user_id: int, bonus_turi: str):
    # bonus_turi: 'vip' yoki 'super'
    # Bu yerda sizning ma'lumotlar bazangizga bonus qo'shish logikasi bo'ladi
    # Misol uchun:
    # if bonus_turi == 'vip':
    #     db.add_bonus(user_id, 1)  # 1 ta telefon raqam olish huquqi
    # elif bonus_turi == 'super':
    #     db.add_bonus(user_id, 3)  # 3 ta telefon raqam olish huquqi
    print(f"User {user_id} uchun {bonus_turi} bonus paketi qo'shildi.")  # DEBUG uchun

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

# VIP aktiv callback — bonus berish bilan
async def vip_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await bonus_paket_qoshish(user_id, 'vip')
    await query.answer()
    await query.edit_message_text(
        "✅ *VIP E'lon aktivlashtirildi!*\n\n"
        "⏰ Muddat: 24 soat\n"
        "🎁 Bonus: 1 marta raqam olish imkoniyati.",
        parse_mode='Markdown'
    )

# Super aktiv callback — bonus berish bilan
async def super_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await bonus_paket_qoshish(user_id, 'super')
    await query.answer()
    await query.edit_message_text(
        "✅ *Super E'lon aktivlashtirildi!*\n\n"
        "⏰ Muddat: 24 soat\n"
        "🎁 Bonus: 3 marta raqam olish imkoniyati.",
        parse_mode='Markdown'
    )

# To'lov uchun tugmalar callback
async def handle_vip_super_tolov(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'vip_tolov':
        await query.edit_message_text("💳 *VIP E'lon uchun to‘lov sahifasi:* https://to'lovlinki/vip\n"
            "💵 Narx: 45,000 so'm",
            parse_mode='Markdown'
        )
    elif query.data == 'super_tolov':
        await query.edit_message_text(
            "💳 *Super E'lon uchun to‘lov sahifasi:* https://to'lovlinki/super\n"
            "💵 Narx: 90,000 so'm",
            parse_mode='Markdown'
        )
