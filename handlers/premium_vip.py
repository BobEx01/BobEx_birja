# handlers/premium_vip.py

from database import cursor, conn
from config import PREMIUM_ELON_NARX, VIP_NARX, ADMIN_ID
from telegram.constants import ParseMode
from datetime import datetime, timedelta

async def premium_elon(update, context):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    if not result or result[0] < PREMIUM_ELON_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. Premium e’lon uchun {PREMIUM_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    # Balansdan yechish
    cursor.execute('UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ? WHERE user_id=?',
                   (PREMIUM_ELON_NARX, PREMIUM_ELON_NARX, user_id))
    conn.commit()

    await update.message.reply_text(
        f"✅ Premium e’lon muvaffaqiyatli faollashtirildi!\n"
        "Endi e’loningiz ro‘yxatda yuqorida chiqadi."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👤 User <code>{user_id}</code> Premium e'lon sotib oldi.",
        parse_mode=ParseMode.HTML
    )


async def vip_aktiv(update, context):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    if not result or result[0] < VIP_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. VIP uchun {VIP_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    vip_muddat = datetime.now() + timedelta(days=30)
    cursor.execute('UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ?, vip_muddati = ? WHERE user_id=?',
                   (VIP_NARX, VIP_NARX, vip_muddat.strftime('%Y-%m-%d'), user_id))
    conn.commit()

    await update.message.reply_text(
        f"🎉 Tabriklaymiz! VIP paket faollashtirildi.\n"
        f"📅 VIP amal qilish muddati: {vip_muddat.strftime('%Y-%m-%d')}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👑 User <code>{user_id}</code> VIP paket sotib oldi. Muddati: {vip_muddat.strftime('%Y-%m-%d')}.",
        parse_mode=ParseMode.HTML
    )
