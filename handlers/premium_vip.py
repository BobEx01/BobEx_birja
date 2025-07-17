from database import cursor, conn
from config import PREMIUM_ELON_NARX, ADMIN_ID
from telegram.constants import ParseMode

async def premium_elon_callback(update, context):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # User balansini tekshirish
    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await query.edit_message_text("❌ Avval ro‘yxatdan o‘ting. /start")
        return

    balans = result[0]
    if balans < PREMIUM_ELON_NARX:
        await query.edit_message_text(
            f"❌ Balansingiz yetarli emas. Premium uchun {PREMIUM_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    # Balansdan yechish
    cursor.execute("""
        UPDATE foydalanuvchilar 
        SET balans = balans - ?, sarflangan = sarflangan + ?
        WHERE user_id = ?
    """, (PREMIUM_ELON_NARX, PREMIUM_ELON_NARX, user_id))
    conn.commit()

    await query.edit_message_text("✅ Premium e'lon muvaffaqiyatli faollashtirildi. E'loningiz yuqorida ko‘rsatiladi.")

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👤 User <code>{user_id}</code> Premium e'lon sotib oldi.",
        parse_mode=ParseMode.HTML
    )
