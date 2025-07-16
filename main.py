# main.py

from telegram.ext import Application, CommandHandler, MessageHandler, filters
import config

async def start(update, context):
    await update.message.reply_text(
        "Assalomu alaykum!\n\n"
        "Quyidagi menyudan tanlang:\n"
        "🚛 Yuk uchun e'lon berish\n"
        "🚚 Shofyor e'lon berish\n"
        "📦 Yuk e'lonlarini ko‘rish\n"
        "🚚 Shofyor e'lonlarini ko‘rish\n"
        "💳 Hisobim\n"
        "🎟 Paketlar\n"
        "❓ Yordam"
    )

app = Application.builder().token(config.TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot ishga tushdi...")
app.run_polling()
