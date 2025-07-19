from telegram import Update
from telegram.ext import ContextTypes

async def premium_va_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔰 E’loningizni yanada samarali qilishni xohlaysizmi?\n\n"
        "📌 Hozirda barcha e’lonlar <b>Tezkor e’lon</b> sifatida <b>BEPUL</b> joylanadi.\n\n"
        "Agar e’loningizni ko‘proq odamlar ko‘rishini istasangiz, quyidagilarni tanlang:\n\n"
        "⭐️ <b>VIP e’lon — 45,000 so‘m</b>\n"
        "• E’lon yonida <b>VIP</b> belgisi.\n"
        "• Kategoriya va viloyat bo‘limlarida doimo yuqorida turadi.\n"
        "• Ko‘rinishlar soni oddiy e’londan <b>5 barobar ko‘p</b>.\n"
        "• BONUS: <b>1 ta telefon raqamni bepul olish</b>.\n\n"
        "🌟 <b>Super e’lon — 90,000 so‘m</b>\n"
        "• E’lon yonida <b>SUPER</b> belgisi.\n"
        "• E’loningiz maxsus <b>Tavsiya qilingan e’lonlar</b> bo‘limida chiqadi.\n"
        "• Ko‘rinishlar soni oddiy e’londan <b>10 barobar ko‘p</b>.\n"
        "• BONUS: <b>3 ta telefon raqamni bepul olish</b>.\n\n"
        "💳 Tanlagan variantingiz uchun quyidagi komandalarni bosing:\n\n"
        "👉 /vip_aktiv — VIP e’lon qilish\n"
        "👉 /super_aktiv — Super e’lon qilish\n"
    )
    await update.message.reply_text(text, parse_mode='HTML')
