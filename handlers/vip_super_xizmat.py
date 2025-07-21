from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# --- Bonus paket qo'shish funksiyasi ---
async def bonus_paket_qoshish(user_id: int, bonus_turi: str):
    if bonus_turi == 'vip':
        bonus_miqdor = 1
    elif bonus_turi == 'super':
        bonus_miqdor = 3
    else:
        bonus_miqdor = 0

    print(f"✅ User {user_id} uchun {bonus_turi} bonus ({bonus_miqdor} ta raqam olish huquqi) qo'shildi.")

# --- VIP E'lon funksiyasi ---
async def vip_elon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔝 *VIP E'lon Xizmati* 🔝\n\n"
        "⭐️ VIP e'loningiz oddiy e'lonlardan har doim yuqorida ko‘rinadi.\n"
        "👀 Ko‘rinishlar soni keskin ortadi.\n"
        "🎯 Ko‘proq mijozlar jalb qilasiz.\n\n"
        "📆 *Amal qilish muddati:* 24 soat\n"
        "🎁 *Bonus:* 1 ta telefon raqam olish imkoniyati\n"
        "💵 *Narxi:* 45,000 so'm\n\n"
        "👇 Quyidagi tugma orqali VIP E'lon xizmatini faollashtiring:"
    )

    buttons = [[InlineKeyboardButton("💳 VIP E'lon uchun to‘lash - 45,000 so'm", callback_data='vip_tolov')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode='Markdown')


# --- SUPER E'lon funksiyasi ---
async def super_elon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 *SUPER E'lon Xizmati* 🚀\n\n"
        "👑 *SUPER* e'lon - barcha e'lonlar orasida eng yuqorida ko‘rsatiladi.\n"
        "🏅 *SUPER* belgisi bilan ajralib turadi.\n"
        "📈 Mijozlar oqimini sezilarli oshiradi.\n\n"
        "📆 *Amal qilish muddati:* 24 soat\n"
        "🎁 *Bonus:* 3 ta telefon raqam olish imkoniyati\n"
        "💵 *Narxi:* 90,000 so'm\n\n"
        "👇 Quyidagi tugma orqali SUPER E'lon xizmatini faollashtiring:"
    )

    buttons = [[InlineKeyboardButton("💳 Super E'lon uchun to‘lash - 90,000 so'm", callback_data='super_tolov')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode='Markdown')


# --- VIP aktiv callback ---
async def vip_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await bonus_paket_qoshish(user_id, 'vip')
    await query.answer()
    await query.edit_message_text(
        "✅ *VIP E'lon aktivlashtirildi!*\n"
        "📆 Amal qilish muddati: 24 soat\n"
        "🎁 Bonus: 1 ta telefon raqam olish imkoniyati\n"
        "📌 E'loningiz har doim ustun joyda ko‘rsatiladi.",
        parse_mode='Markdown'
    )


# --- Super aktiv callback ---
async def super_aktiv_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await bonus_paket_qoshish(user_id, 'super')
    await query.answer()
    await query.edit_message_text(
        "✅ *Super E'lon aktivlashtirildi!*\n"
        "📆 Amal qilish muddati: 24 soat\n"
        "🎁 Bonus: 3 ta telefon raqam olish imkoniyati\n"
        "🚀 E'loningiz barcha e'lonlardan yuqorida ko‘rsatiladi.",
        parse_mode='Markdown'
    )


# --- To'lov uchun tugmalar callback ---
async def handle_vip_super_tolov(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'vip_tolov':
        await query.edit_message_text(
            "💳 *VIP E'lon uchun to‘lov sahifasi:*\n"
            "👉 [VIP To‘lov Sahifasi](https://to'lovlinki/vip)\n\n"
            "💵 Narxi: 45,000 so'm\n"
            "📆 Muddat: 24 soat\n"
            "🎁 Bonus: 1 ta telefon raqam olish imkoniyati",
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    elif query.data == 'super_tolov':
        await query.edit_message_text(
            "💳 *Super E'lon uchun to‘lov sahifasi:*\n"
            "👉 [Super To‘lov Sahifasi](https://to'lovlinki/super)\n\n"
            "💵 Narxi: 90,000 so'm\n"
            "📆 Muddat: 24 soat\n"
            "🎁 Bonus: 3 ta telefon raqam olish imkoniyati",
            parse_mode='Markdown',disable_web_page_preview=True
        )
