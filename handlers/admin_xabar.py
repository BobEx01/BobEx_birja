# handlers/admin_xabar.py

ADMIN_ID = 8080091052  # Sizning Telegram ID'ingiz
ADMIN_USERNAME = '@bobex_uz'  # Sizning Telegram username'ingiz

async def admin_xabar(context, text, user=None):
    """
    Admin Muhammadbobur uchun avtomatik xabar yuborish.
    """
    user_info = ""
    if user:
        username = f"@{user.username}" if user.username else "Username yo‘q"
        user_info = (
            f"\n👤 Foydalanuvchi: {username}\n"
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
