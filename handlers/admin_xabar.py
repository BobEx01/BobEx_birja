# handlers/admin_xabar.py

from telegram import Update
from telegram.ext import ContextTypes

ADMIN_ID = 8080091052  # Sizning Telegram ID'ingiz
ADMIN_USERNAME = '@bobex_uz'  # Sizning Telegram username'ingiz

async def admin_xabar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    user_info = (
        f"\n👤 Foydalanuvchi: @{user.username if user.username else 'Username yo‘q'}\n"
        f"🆔 ID: {user.id}\n"
        f"📝 Ismi: {user.first_name}"
    )
    
    final_text = (
        f"📢 <b>Admin uchun xabar:</b>\n\n"
        f"{text}\n"
        f"{user_info}\n"
        f"👮‍♂️ Admin: {ADMIN_USERNAME} | ID: {ADMIN_ID}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=final_text,
        parse_mode='HTML'
    )

    await update.message.reply_text("✅ Xabaringiz adminga yuborildi.")
