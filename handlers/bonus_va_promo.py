from telegram import Update
from telegram.ext import ContextTypes

async def elon_bonus_taklif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✅ Sizning e'loningiz <b>\"Tezkor e'lon\"</b> sifatida <b>bepul</b> joylandi.\n\n"
        "Agar e'loningizni ko‘proq odamlar ko‘rishini xohlasangiz va <b>telefon raqamlarni bepul olish bonusiga</b> ega bo‘lishni istasangiz, quyidagilarni tanlang:\n\n"
        "🔸 <b>VIP e’lon — 45,000 so‘m</b>\n"
        "• E'lon yonida <b>VIP</b> belgisi.\n"
        "• Viloyat va tuman bo‘limlarida <b>birinchi sahifada</b> chiqadi.\n"
        "• Ko‘rinishlar soni oddiy e'londan <b>5 barobar ko‘p</b>.\n"
        "• <b>Bonus:</b> 1 ta telefon raqamni <b>bepul</b> olish.\n\n"
        "🌟 <b>Super e’lon — 90,000 so‘m</b>\n"
        "• E'lon yonida <b>SUPER</b> belgisi.\n"
        "• Doim yuqori qismda va <b>maxsus tavsiya blokida</b>.\n"
        "• Ko‘rinishlar soni oddiy e'londan <b>10 barobar ko‘p</b>.\n"
        "• <b>Bonus:</b> 3 ta telefon raqamni <b>bepul</b> olish.\n\n"
        "💰 <i>Tezkor, VIP yoki Super e’lon uchun quyidagilardan foydalaning:</i>\n\n"
        "👉 /vip_aktiv — VIP e’lon qilish\n"
        "👉 /super_aktiv — Super e’lon qilish"
    )
    await update.message.reply_text(text, parse_mode='HTML')
