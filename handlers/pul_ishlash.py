from telegram import Update
from telegram.ext import ContextTypes

async def pul_ishlash_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    bot_username = (await context.bot.get_me()).username
    referal_link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"💸 *Pul ishlash bo‘limi*\n\n"
        f"Quyidagi referal linkni do‘stlaringizga yuboring:\n"
        f"{referal_link}\n\n"
        f"Har bir taklifingiz uchun 2000 so‘m bonus olasiz!",
        parse_mode='Markdown'
    )
