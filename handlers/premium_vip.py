# handlers/premium_vip.py

from database import cursor, conn
from config import PREMIUM_ELON_NARX, VIP_NARX
import datetime

async def premium_elon(update, context):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM users WHERE telegram_id=?', (user_id,))
    result = cursor.fetchone()
    if not result or result[0] < PREMIUM_ELON_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. Premium e’lon uchun {PREMIUM_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    # Premium elon uchun balansdan yechish
    cursor.execute('UPDATE users SET balans = balans - ?, sarflangan = sarflangan + ? WHERE telegram_id=?',
                   (PREMIUM_ELON_NARX, PREMIUM_ELON_NARX, user_id))
    conn.commit()

    await update.message.reply_text(
        f"✅ Premium e’lon muvaffaqiyatli faollashtirildi!\n"
        "Endi e’loningiz ro‘yxatda yuqorida chiqadi."
    )

async def vip_aktiv(update, context):
    user_id = update.message.from_user.id
    cursor.execute('SELECT balans FROM users WHERE telegram_id=?', (user_id,))
    result = cursor.fetchone()

    if not result or result[0] < VIP_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. VIP olish uchun {VIP_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    # VIP olish uchun balansdan yechish
    cursor.execute('UPDATE users SET balans = balans - ?, sarflangan = sarflangan + ?, vip=1, vip_muddat=? WHERE telegram_id=?',
                   (VIP_NARX, VIP_NARX, datetime.datetime.now().strftime("%Y-%m-%d"), user_id))
    conn.commit()

    await update.message.reply_text(
        "👑 VIP statusingiz 30 kun davomida faollashtirildi!\n\n"
        "VIP bo‘lsangiz barcha funksiyalar bepul bo‘ladi."
    )
