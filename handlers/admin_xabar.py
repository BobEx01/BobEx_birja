# handlers/admin_xabar.py

from config import ADMIN_ID

async def admin_xabar(context, text):
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
